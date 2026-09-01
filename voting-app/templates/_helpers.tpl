{{/* Common name */}}
{{- define "voting-app.fullname" -}}
{{- .Release.Name -}}
{{- end -}}

{{/* Common labels */}}
{{- define "voting-app.labels" -}}
app.kubernetes.io/part-of: voting-app
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}
