{{- define "demo-linkops.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "demo-linkops.fullname" -}}
{{- if .Values.fullnameOverride }}
{{-   .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{-   printf "%s-%s" (include "demo-linkops.name" .) .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }} 