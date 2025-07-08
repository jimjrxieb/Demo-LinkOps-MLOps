{{/*
Expand the name of the chart.
*/}}
{{- define "linkops.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "linkops.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "linkops.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "linkops.labels" -}}
helm.sh/chart: {{ include "linkops.chart" . }}
{{ include "linkops.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "linkops.selectorLabels" -}}
app.kubernetes.io/name: {{ include "linkops.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the config map to use
*/}}
{{- define "linkops.configMapName" -}}
{{- printf "%s-config" (include "linkops.fullname" .) }}
{{- end }}

{{/*
Create the name of the secret to use
*/}}
{{- define "linkops.secretName" -}}
{{- printf "%s-secret" (include "linkops.fullname" .) }}
{{- end }}

{{/*
Create the name of the service to use
*/}}
{{- define "linkops.serviceName" -}}
{{- printf "%s" (include "linkops.fullname" .) }}
{{- end }}

{{/*
Create the name of the deployment to use
*/}}
{{- define "linkops.deploymentName" -}}
{{- printf "%s" (include "linkops.fullname" .) }}
{{- end }}

{{/*
Create the name of the ingress to use
*/}}
{{- define "linkops.ingressName" -}}
{{- printf "%s" (include "linkops.fullname" .) }}
{{- end }}

{{/*
Create the name of the HPA to use
*/}}
{{- define "linkops.hpaName" -}}
{{- printf "%s-hpa" (include "linkops.fullname" .) }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "linkops.serviceAccountName" -}}
{{- if .Values.security.rbac.createServiceAccounts }}
{{- printf "%s-sa" (include "linkops.fullname" .) }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the role to use
*/}}
{{- define "linkops.roleName" -}}
{{- printf "%s-role" (include "linkops.fullname" .) }}
{{- end }}

{{/*
Create the name of the role binding to use
*/}}
{{- define "linkops.roleBindingName" -}}
{{- printf "%s-rolebinding" (include "linkops.fullname" .) }}
{{- end }}

{{/*
Create the name of the network policy to use
*/}}
{{- define "linkops.networkPolicyName" -}}
{{- printf "%s-network-policy" (include "linkops.fullname" .) }}
{{- end }}

{{/*
Create the name of the PVC to use
*/}}
{{- define "linkops.pvcName" -}}
{{- printf "%s-pvc" (include "linkops.fullname" .) }}
{{- end }}

{{/*
Create the name of the config map to use for a specific service
*/}}
{{- define "linkops.serviceConfigMapName" -}}
{{- printf "%s-config" . }}
{{- end }}

{{/*
Create the name of the secret to use for a specific service
*/}}
{{- define "linkops.serviceSecretName" -}}
{{- printf "%s-secret" . }}
{{- end }}

{{/*
Create the name of the service to use for a specific service
*/}}
{{- define "linkops.serviceServiceName" -}}
{{- printf "%s" . }}
{{- end }}

{{/*
Create the name of the deployment to use for a specific service
*/}}
{{- define "linkops.serviceDeploymentName" -}}
{{- printf "%s" . }}
{{- end }}

{{/*
Create the name of the ingress to use for a specific service
*/}}
{{- define "linkops.serviceIngressName" -}}
{{- printf "%s" . }}
{{- end }}

{{/*
Create the name of the HPA to use for a specific service
*/}}
{{- define "linkops.serviceHpaName" -}}
{{- printf "%s-hpa" . }}
{{- end }}

{{/*
Create the name of the service account to use for a specific service
*/}}
{{- define "linkops.serviceServiceAccountName" -}}
{{- printf "%s-sa" . }}
{{- end }}

{{/*
Create the name of the role to use for a specific service
*/}}
{{- define "linkops.serviceRoleName" -}}
{{- printf "%s-role" . }}
{{- end }}

{{/*
Create the name of the role binding to use for a specific service
*/}}
{{- define "linkops.serviceRoleBindingName" -}}
{{- printf "%s-rolebinding" . }}
{{- end }}

{{/*
Create the name of the network policy to use for a specific service
*/}}
{{- define "linkops.serviceNetworkPolicyName" -}}
{{- printf "%s-network-policy" . }}
{{- end }}

{{/*
Create the name of the PVC to use for a specific service
*/}}
{{- define "linkops.servicePvcName" -}}
{{- printf "%s-pvc" . }}
{{- end }} 