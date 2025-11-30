// Copyright (C) 2025 AIDC-AI (original)
// Copyright (C) 2025 DataSparBrian (fork modifications)
// Licensed under the MIT License.

const isDevelopment = import.meta.env.MODE === 'development'

const defaultApiBaseUrl = 'http://localhost:8000'

// Privacy-focused fork: Updated to point to ComfyUI-Copilot-Unboxed repository
export const github_url = 'https://github.com/DataSparBrian/ComfyUI-Copilot-Unboxed'

export const config = {
  apiBaseUrl: isDevelopment
    ? defaultApiBaseUrl
    : (import.meta.env.VITE_API_BASE_URL || defaultApiBaseUrl)
} 