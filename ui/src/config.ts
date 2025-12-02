// Copyright (C) 2025 AIDC-AI (original)
// Copyright (C) 2025 DataSparBrian (fork modifications)
// Licensed under the MIT License.

// Privacy-focused fork: LLM endpoint configuration
// Users configure their LLM endpoint via the Settings UI (ApiKeyModal)
// The endpoint is stored in localStorage as 'workflowLLMBaseUrl'
// No hardcoded defaults - user must configure their own LLM service

const getApiBaseUrl = (): string => {
  // Read from user configuration in localStorage
  const userConfiguredUrl = localStorage.getItem('workflowLLMBaseUrl');

  if (userConfiguredUrl) {
    return userConfiguredUrl;
  }

  // Fallback for development/testing only - can be overridden via env var
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }

  // No default - return empty string
  // UI will prompt user to configure their LLM endpoint
  return '';
};

// Privacy-focused fork: Updated to point to ComfyUI-Copilot-Unboxed repository
export const github_url = 'https://github.com/DataSparBrian/ComfyUI-Copilot-Unboxed'

export const config = {
  get apiBaseUrl(): string {
    return getApiBaseUrl();
  }
} 