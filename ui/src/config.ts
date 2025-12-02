// Copyright (C) 2025 AIDC-AI (original)
// Copyright (C) 2025 DataSparBrian (fork modifications)
// Licensed under the MIT License.

// Privacy-focused fork: LLM endpoint configuration
// Set VITE_API_BASE_URL environment variable to point to your LLM service
// Example: VITE_API_BASE_URL=http://localhost:8001 npm run build
const defaultApiBaseUrl = 'http://localhost:8000'

// Privacy-focused fork: Updated to point to ComfyUI-Copilot-Unboxed repository
export const github_url = 'https://github.com/DataSparBrian/ComfyUI-Copilot-Unboxed'

export const config = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || defaultApiBaseUrl
} 