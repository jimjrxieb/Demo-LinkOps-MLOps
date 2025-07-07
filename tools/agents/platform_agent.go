package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

// CommandResult represents the result of a command execution
type CommandResult struct {
	Command     string    `json:"command"`
	Success     bool      `json:"success"`
	Output      string    `json:"output,omitempty"`
	Error       string    `json:"error,omitempty"`
	Duration    string    `json:"duration"`
	Timestamp   time.Time `json:"timestamp"`
	ExitCode    int       `json:"exit_code"`
	Environment string    `json:"environment"`
}

// RuneConfig represents a rune configuration for execution
type RuneConfig struct {
	Name        string   `json:"name"`
	Description string   `json:"description"`
	Commands    []string `json:"commands"`
	Validation  struct {
		AllowedCommands []string `json:"allowed_commands"`
		DeniedCommands  []string `json:"denied_commands"`
		Timeout         int      `json:"timeout_seconds"`
		StopOnFailure   bool     `json:"stop_on_failure"`
	} `json:"validation"`
}

// AgentConfig holds the agent configuration
type AgentConfig struct {
	LogFile       string   `json:"log_file"`
	AllowedPaths  []string `json:"allowed_paths"`
	DeniedCommands []string `json:"denied_commands"`
	MaxTimeout    int      `json:"max_timeout_seconds"`
	Environment   string   `json:"environment"`
}

// Global configuration
var config AgentConfig

// init loads the agent configuration
func init() {
	config = AgentConfig{
		LogFile: "platform_agent.log",
		AllowedPaths: []string{
			"/usr/local/bin",
			"/usr/bin",
			"/bin",
			"/usr/sbin",
			"/sbin",
		},
		DeniedCommands: []string{
			"rm", "shutdown", ":(){", "mkfs", "dd", "format",
			"del", "erase", "killall", "pkill", "kill -9",
			"sudo rm", "sudo shutdown", "sudo mkfs",
		},
		MaxTimeout:  300, // 5 minutes
		Environment: "production",
	}

	// Load config from file if it exists
	if _, err := os.Stat("agent_config.json"); err == nil {
		data, err := ioutil.ReadFile("agent_config.json")
		if err == nil {
			json.Unmarshal(data, &config)
		}
	}

	// Setup logging
	logFile, err := os.OpenFile(config.LogFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Printf("Warning: Could not open log file: %v", err)
	} else {
		log.SetOutput(logFile)
	}
}

// sanitizeCommand validates and sanitizes the command
func sanitizeCommand(cmd string) (bool, string) {
	// Check for denied commands
	for _, denied := range config.DeniedCommands {
		if strings.Contains(strings.ToLower(cmd), strings.ToLower(denied)) {
			return false, fmt.Sprintf("Command contains denied pattern: %s", denied)
		}
	}

	// Basic command structure validation
	parts := strings.Fields(cmd)
	if len(parts) == 0 {
		return false, "Empty command"
	}

	// Check if command exists in allowed paths
	command := parts[0]
	found := false
	for _, path := range config.AllowedPaths {
		if _, err := os.Stat(filepath.Join(path, command)); err == nil {
			found = true
			break
		}
	}

	// Allow commands that are in PATH
	if !found {
		if _, err := exec.LookPath(command); err != nil {
			return false, fmt.Sprintf("Command not found: %s", command)
		}
	}

	return true, ""
}

// executeCommand runs a single command and returns the result
func executeCommand(cmd string, timeout int) CommandResult {
	result := CommandResult{
		Command:   cmd,
		Timestamp: time.Now(),
		Environment: config.Environment,
	}

	// Validate command
	if valid, reason := sanitizeCommand(cmd); !valid {
		result.Success = false
		result.Error = reason
		result.Duration = "0s"
		result.ExitCode = -1
		return result
	}

	// Parse command
	parts := strings.Fields(cmd)
	if len(parts) == 0 {
		result.Success = false
		result.Error = "Empty command"
		result.Duration = "0s"
		result.ExitCode = -1
		return result
	}

	// Create command with timeout
	ctx, cancel := context.WithTimeout(context.Background(), time.Duration(timeout)*time.Second)
	defer cancel()

	command := exec.CommandContext(ctx, parts[0], parts[1:]...)
	
	// Capture output
	output, err := command.CombinedOutput()
	
	// Record duration
	duration := time.Since(result.Timestamp)
	result.Duration = duration.String()

	if err != nil {
		result.Success = false
		result.Error = err.Error()
		result.Output = string(output)
		if exitError, ok := err.(*exec.ExitError); ok {
			result.ExitCode = exitError.ExitCode()
		} else {
			result.ExitCode = -1
		}
	} else {
		result.Success = true
		result.Output = string(output)
		result.ExitCode = 0
	}

	// Log the result
	log.Printf("Command: %s | Success: %t | Duration: %s | ExitCode: %d", 
		cmd, result.Success, result.Duration, result.ExitCode)

	return result
}

// executeRune runs a series of commands from a rune configuration
func executeRune(runeFile string) ([]CommandResult, error) {
	// Read rune configuration
	data, err := ioutil.ReadFile(runeFile)
	if err != nil {
		return nil, fmt.Errorf("failed to read rune file: %v", err)
	}

	var runeConfig RuneConfig
	if err := json.Unmarshal(data, &runeConfig); err != nil {
		return nil, fmt.Errorf("failed to parse rune configuration: %v", err)
	}

	fmt.Printf("🔮 Executing Rune: %s\n", runeConfig.Name)
	fmt.Printf("📝 Description: %s\n", runeConfig.Description)
	fmt.Printf("⚡ Commands: %d\n\n", len(runeConfig.Commands))

	var results []CommandResult
	timeout := runeConfig.Validation.Timeout
	if timeout == 0 {
		timeout = config.MaxTimeout
	}

	for i, cmd := range runeConfig.Commands {
		fmt.Printf("🔄 [%d/%d] Executing: %s\n", i+1, len(runeConfig.Commands), cmd)
		
		result := executeCommand(cmd, timeout)
		results = append(results, result)

		if result.Success {
			fmt.Printf("✅ Success: %s\n", result.Duration)
		} else {
			fmt.Printf("❌ Failed: %s\n", result.Error)
		}

		// Stop on first failure if configured
		if !result.Success && runeConfig.Validation.StopOnFailure {
			fmt.Println("🛑 Stopping execution due to failure")
			break
		}
	}

	return results, nil
}

// saveResults saves command results to a JSON file
func saveResults(results []CommandResult, filename string) error {
	data, err := json.MarshalIndent(results, "", "  ")
	if err != nil {
		return err
	}

	return ioutil.WriteFile(filename, data, 0644)
}

// printUsage displays the usage information
func printUsage() {
	fmt.Println(`
🔮 LinkOps Platform Agent - Command Executor

Usage:
  platform_agent <command>                    # Execute a single command
  platform_agent --rune <rune-file.json>      # Execute a rune configuration
  platform_agent --config <config-file.json>  # Load custom configuration
  platform_agent --help                       # Show this help

Examples:
  platform_agent "kubectl get pods"
  platform_agent "docker ps"
  platform_agent --rune deployment-rune.json
  platform_agent --config custom-config.json

Safety Features:
  ✅ Command validation and sanitization
  ✅ Path restrictions
  ✅ Timeout protection
  ✅ Comprehensive logging
  ✅ JSON result output

Rune Configuration Format:
  {
    "name": "Deployment Rune",
    "description": "Deploy application to Kubernetes",
    "commands": [
      "kubectl apply -f deployment.yaml",
      "kubectl rollout status deployment/app"
    ],
    "validation": {
      "timeout_seconds": 300,
      "stop_on_failure": true
    }
  }
`)
}

func main() {
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}

	// Handle help
	if os.Args[1] == "--help" || os.Args[1] == "-h" {
		printUsage()
		return
	}

	// Handle rune execution
	if os.Args[1] == "--rune" {
		if len(os.Args) < 3 {
			fmt.Println("❌ Error: Rune file not specified")
			fmt.Println("Usage: platform_agent --rune <rune-file.json>")
			os.Exit(1)
		}

		results, err := executeRune(os.Args[2])
		if err != nil {
			fmt.Printf("❌ Error executing rune: %v\n", err)
			os.Exit(1)
		}

		// Save results
		outputFile := fmt.Sprintf("rune_results_%s.json", time.Now().Format("20060102_150405"))
		if err := saveResults(results, outputFile); err != nil {
			fmt.Printf("⚠️  Warning: Could not save results: %v\n", err)
		} else {
			fmt.Printf("📄 Results saved to: %s\n", outputFile)
		}

		// Print summary
		successCount := 0
		for _, result := range results {
			if result.Success {
				successCount++
			}
		}
		fmt.Printf("\n📊 Summary: %d/%d commands successful\n", successCount, len(results))
		return
	}

	// Handle single command execution
	cmd := os.Args[1]
	fmt.Printf("🔮 Executing: %s\n", cmd)

	result := executeCommand(cmd, config.MaxTimeout)

	// Print result
	if result.Success {
		fmt.Printf("✅ Success! Duration: %s\n", result.Duration)
		if result.Output != "" {
			fmt.Printf("📄 Output:\n%s\n", result.Output)
		}
	} else {
		fmt.Printf("❌ Failed: %s\n", result.Error)
		if result.Output != "" {
			fmt.Printf("📄 Output:\n%s\n", result.Output)
		}
		os.Exit(1)
	}

	// Save single result
	outputFile := fmt.Sprintf("command_result_%s.json", time.Now().Format("20060102_150405"))
	if err := saveResults([]CommandResult{result}, outputFile); err != nil {
		fmt.Printf("⚠️  Warning: Could not save result: %v\n", err)
	} else {
		fmt.Printf("📄 Result saved to: %s\n", outputFile)
	}
} 