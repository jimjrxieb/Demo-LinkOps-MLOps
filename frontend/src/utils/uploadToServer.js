/**
 * File upload utilities for CSV files
 * Handles file validation, upload progress, and error handling
 */

/**
 * Validate CSV file before upload
 * @param {File} file - The file to validate
 * @returns {Object} Validation result with success and message
 */
export const validateCsvFile = (file) => {
  // Check file type
  if (!file.type.includes('csv') && !file.name.endsWith('.csv')) {
    return {
      success: false,
      message: 'Please select a valid CSV file',
    };
  }

  // Check file size (max 10MB)
  const maxSize = 10 * 1024 * 1024; // 10MB
  if (file.size > maxSize) {
    return {
      success: false,
      message: 'File size must be less than 10MB',
    };
  }

  // Check if file is empty
  if (file.size === 0) {
    return {
      success: false,
      message: 'File cannot be empty',
    };
  }

  return {
    success: true,
    message: 'File is valid',
  };
};

/**
 * Parse CSV headers from file content
 * @param {string} content - CSV file content
 * @returns {Array} Array of header names
 */
export const parseCsvHeaders = (content) => {
  try {
    const lines = content.split('\n');
    if (lines.length === 0) {
      throw new Error('Empty file');
    }

    const firstLine = lines[0].trim();
    if (!firstLine) {
      throw new Error('No headers found');
    }

    // Split by comma and clean up headers
    const headers = firstLine
      .split(',')
      .map((header) => header.trim().replace(/"/g, '').replace(/'/g, ''));

    // Filter out empty headers
    const validHeaders = headers.filter((header) => header.length > 0);

    if (validHeaders.length === 0) {
      throw new Error('No valid headers found');
    }

    return validHeaders;
  } catch (error) {
    console.error('Error parsing CSV headers:', error);
    throw new Error('Invalid CSV format: ' + error.message);
  }
};

/**
 * Upload CSV file to server
 * @param {File} file - The file to upload
 * @param {Function} onProgress - Progress callback function
 * @param {string} endpoint - Upload endpoint URL
 * @returns {Promise} Upload result
 */
export const uploadCsvToServer = async (
  file,
  onProgress = null,
  endpoint = '/api/upload-csv'
) => {
  try {
    // Validate file first
    const validation = validateCsvFile(file);
    if (!validation.success) {
      throw new Error(validation.message);
    }

    // Create FormData
    const formData = new FormData();
    formData.append('file', file);

    // Create XMLHttpRequest for progress tracking
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();

      // Progress tracking
      if (onProgress) {
        xhr.upload.addEventListener('progress', (event) => {
          if (event.lengthComputable) {
            const percentComplete = (event.loaded / event.total) * 100;
            onProgress(percentComplete, 'Uploading...');
          }
        });
      }

      // Handle response
      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          try {
            const response = JSON.parse(xhr.responseText);
            resolve(response);
          } catch (error) {
            reject(new Error('Invalid response format'));
          }
        } else {
          reject(new Error(`Upload failed: ${xhr.status} ${xhr.statusText}`));
        }
      });

      // Handle errors
      xhr.addEventListener('error', () => {
        reject(new Error('Network error during upload'));
      });

      xhr.addEventListener('abort', () => {
        reject(new Error('Upload was cancelled'));
      });

      // Send request
      xhr.open('POST', endpoint);
      xhr.send(formData);
    });
  } catch (error) {
    console.error('Upload error:', error);
    throw error;
  }
};

/**
 * Upload CSV file using fetch API (simpler, no progress)
 * @param {File} file - The file to upload
 * @param {string} endpoint - Upload endpoint URL
 * @returns {Promise} Upload result
 */
export const uploadCsvWithFetch = async (
  file,
  endpoint = '/api/upload-csv'
) => {
  try {
    // Validate file first
    const validation = validateCsvFile(file);
    if (!validation.success) {
      throw new Error(validation.message);
    }

    // Create FormData
    const formData = new FormData();
    formData.append('file', file);

    // Send request
    const response = await fetch(endpoint, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `Upload failed: ${response.status} ${response.statusText} - ${errorText}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error('Upload error:', error);
    throw error;
  }
};

/**
 * Preview CSV data (first few rows)
 * @param {File} file - The CSV file to preview
 * @param {number} maxRows - Maximum number of rows to preview
 * @returns {Promise} Preview data
 */
export const previewCsvData = async (file, maxRows = 5) => {
  try {
    const text = await file.text();
    const lines = text.split('\n').filter((line) => line.trim());

    if (lines.length === 0) {
      throw new Error('Empty file');
    }

    const headers = parseCsvHeaders(lines[0]);
    const dataRows = lines.slice(1, maxRows + 1).map((line) => {
      const values = line.split(',').map((val) => val.trim().replace(/"/g, ''));
      const row = {};
      headers.forEach((header, index) => {
        row[header] = values[index] || '';
      });
      return row;
    });

    return {
      headers,
      data: dataRows,
      totalRows: lines.length - 1,
    };
  } catch (error) {
    console.error('Error previewing CSV:', error);
    throw error;
  }
};

/**
 * Format file size for display
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted file size
 */
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

/**
 * Generate sample CSV data for testing
 * @returns {string} Sample CSV content
 */
export const generateSampleCsv = () => {
  const headers = [
    'property_id',
    'property_type',
    'age_years',
    'square_feet',
    'contractor',
    'maintenance_type',
    'completion_time',
    'cost',
    'quality_score',
    'monthly_cost',
  ];

  const sampleData = [
    [1, 'apartment', 5, 800, 'Contractor A', 'plumbing', 2, 500, 8, 150],
    [2, 'house', 10, 1200, 'Contractor B', 'electrical', 3, 750, 7, 200],
    [3, 'condo', 15, 1500, 'Contractor C', 'hvac', 4, 1000, 9, 250],
    [4, 'apartment', 20, 2000, 'Contractor D', 'roofing', 5, 1250, 6, 300],
    [5, 'house', 25, 2500, 'Contractor E', 'general', 6, 1500, 8, 350],
  ];

  const csvContent = [
    headers.join(','),
    ...sampleData.map((row) => row.join(',')),
  ].join('\n');

  return csvContent;
};

/**
 * Download sample CSV file
 */
export const downloadSampleCsv = () => {
  const csvContent = generateSampleCsv();
  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);

  const link = document.createElement('a');
  link.href = url;
  link.download = 'sample_property_data.csv';
  link.click();

  URL.revokeObjectURL(url);
};

/**
 * Check if browser supports file upload features
 * @returns {Object} Support status for various features
 */
export const checkUploadSupport = () => {
  return {
    fileApi: typeof File !== 'undefined',
    formData: typeof FormData !== 'undefined',
    xhr: typeof XMLHttpRequest !== 'undefined',
    fetch: typeof fetch !== 'undefined',
    fileReader: typeof FileReader !== 'undefined',
    dragAndDrop: 'draggable' in document.createElement('div'),
  };
};
