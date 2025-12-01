// Copyright (C) 2025 AIDC-AI (original)
// Copyright (C) 2025 DataSparBrian (fork modifications)
// Licensed under the MIT License.

const isDevelopment = import.meta.env.MODE === 'development'

// Privacy-focused fork: Runtime detection of ComfyUI server URL
// This fixes the hardcoded port issue - ComfyUI can run on any port
// We detect it from the current page origin at runtime
const getApiBaseUrl = () => {
  // In development, allow override via env var, otherwise use current origin
  if (isDevelopment && import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }

  // Production or no override: use the current page's origin
  // This automatically works regardless of ComfyUI's port
  return window.location.origin;
}

// Privacy-focused fork: Updated to point to ComfyUI-Copilot-Unboxed repository
export const github_url = 'https://github.com/DataSparBrian/ComfyUI-Copilot-Unboxed'

export const config = {
  apiBaseUrl: getApiBaseUrl()
} 