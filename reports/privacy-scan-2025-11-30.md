# Privacy Validation Report
Generated: 2025-11-30 21:19:58
============================================================

## Summary

- ❌ **Critical**: 19
- 🚨 **Errors**: 6
- ⚠️  **Warnings**: 14
- **Total**: 39

**Status**: ❌ FAILED - Privacy violations found

## ❌ Critical Violations

### Analytics Call (18)

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/apis/workflowChatApi.ts:69**
  - Analytics function call detected
  - ```export async function trackEvent(```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/apis/workflowChatApi.ts:154**
  - Analytics function call detected
  - ```trackEvent({```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/chat/ModelDownloadModal.tsx:35**
  - Analytics function call detected
  - ```WorkflowChatAPI.trackEvent({```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/chat/ChatInput.tsx:207**
  - Analytics function call detected
  - ```WorkflowChatAPI.trackEvent({```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/chat/ChatInput.tsx:270**
  - Analytics function call detected
  - ```WorkflowChatAPI.trackEvent({```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/chat/messages/ModelOption.tsx:86**
  - Analytics function call detected
  - ```WorkflowChatAPI.trackEvent({```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/chat/messages/NodeSearch.tsx:82**
  - Analytics function call detected
  - ```WorkflowChatAPI.trackEvent({```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/chat/messages/NodeSearch.tsx:136**
  - Analytics function call detected
  - ```WorkflowChatAPI.trackEvent({```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/chat/messages/NodeSearch.tsx:160**
  - Analytics function call detected
  - ```WorkflowChatAPI.trackEvent({```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/chat/messages/DownstreamSubgraphs.tsx:139**
  - Analytics function call detected
  - ```WorkflowChatAPI.trackEvent({```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/chat/messages/DebugGuide.tsx:75**
  - Analytics function call detected
  - ```WorkflowChatAPI.trackEvent({```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/chat/messages/WorkflowOption.tsx:57**
  - Analytics function call detected
  - ```WorkflowChatAPI.trackEvent({```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/debug/utils/imageGenerationUtils.ts:58**
  - Analytics function call detected
  - ```WorkflowChatAPI.trackEvent({```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/debug/utils/stateManagementUtils.ts:152**
  - Analytics function call detected
  - ```WorkflowChatAPI.trackEvent({```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/debug/utils/aiTextUtils.ts:32**
  - Analytics function call detected
  - ```WorkflowChatAPI.trackEvent({```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/debug/utils/aiTextUtils.ts:103**
  - Analytics function call detected
  - ```WorkflowChatAPI.trackEvent({```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/ui/Markdown.tsx:153**
  - Analytics function call detected
  - ```WorkflowChatAPI.trackEvent({```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/ui/RestoreCheckpoint.tsx:24**
  - Analytics function call detected
  - ```WorkflowChatAPI.trackEvent({```

### Email Collection (1)

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/chat/ApiKeyModal.tsx:251**
  - Email collection pattern detected
  - ```const response = await fetch(`${BASE_URL}/api/user/create`, {```

## 🚨 Errors

### Api Key Generation (2)

- **/home/user/ComfyUI-Copilot-Unboxed/tools/privacy_validator.py:320**
  - Vendor API key generation detected
  - ```r"/api/key/generate",```

- **/home/user/ComfyUI-Copilot-Unboxed/tools/privacy_validator.py:321**
  - Vendor API key generation detected
  - ```r"/api/key/create",```

### Vendor Cdn (4)

- **/home/user/ComfyUI-Copilot-Unboxed/docs/maintenance/MODIFICATION_MANIFEST.json:311**
  - Vendor CDN URL detected: alibaba
  - ```"url": "https://cdn.contract.alibaba.com/terms/privacy_policy_full/...",```

- **/home/user/ComfyUI-Copilot-Unboxed/docs/maintenance/MODIFICATION_MANIFEST.json:318**
  - Vendor CDN URL detected: alibaba
  - ```"url": "https://cdn.contract.alibaba.com/terms/c_end_product_protocol/...",```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/chat/ApiKeyModal.tsx:366**
  - Vendor CDN URL detected: alibaba
  - ```href="https://cdn.contract.alibaba.com/terms/privacy_policy_full/202502191459588```

- **/home/user/ComfyUI-Copilot-Unboxed/ui/src/components/chat/ApiKeyModal.tsx:374**
  - Vendor CDN URL detected: alibaba
  - ```href="https://cdn.contract.alibaba.com/terms/c_end_product_protocol/202502191502```

## ⚠️ Warnings

### Email Collection (9)

- **/home/user/ComfyUI-Copilot-Unboxed/tools/privacy_validator.py:223**
  - Email collection pattern detected
  - ```r"email.*validation",```

- **/home/user/ComfyUI-Copilot-Unboxed/tools/privacy_validator.py:224**
  - Email collection pattern detected
  - ```r"/api/user/create",```

- **/home/user/ComfyUI-Copilot-Unboxed/tools/privacy_validator.py:225**
  - Email collection pattern detected
  - ```r"/api/auth/register",```

- **/home/user/ComfyUI-Copilot-Unboxed/tools/privacy_validator.py:226**
  - Email collection pattern detected
  - ```r"collect.*email",```

- **/home/user/ComfyUI-Copilot-Unboxed/tools/privacy_validator.py:227**
  - Email collection pattern detected
  - ```r"register.*email",```

- **/home/user/ComfyUI-Copilot-Unboxed/tools/upstream_monitor.py:243**
  - Email collection pattern detected
  - ```"email_collection": r"(email.*validation|collect.*email|user.*create|registratio```

- **/home/user/ComfyUI-Copilot-Unboxed/tools/upstream_monitor.py:243**
  - Email collection pattern detected
  - ```"email_collection": r"(email.*validation|collect.*email|user.*create|registratio```

- **/home/user/ComfyUI-Copilot-Unboxed/docs/maintenance/MODIFICATION_MANIFEST.json:56**
  - Email collection pattern detected
  - ```"description": "Remove handleSendEmail function that POSTs to /api/user/create",```

- **/home/user/ComfyUI-Copilot-Unboxed/docs/maintenance/MODIFICATION_MANIFEST.json:302**
  - Email collection pattern detected
  - ```"endpoint": "/api/user/create",```

### Forced Registration (5)

- **/home/user/ComfyUI-Copilot-Unboxed/tools/privacy_validator.py:295**
  - Potential forced registration pattern
  - ```r"require.*registration",```

- **/home/user/ComfyUI-Copilot-Unboxed/tools/privacy_validator.py:296**
  - Potential forced registration pattern
  - ```r"force.*register",```

- **/home/user/ComfyUI-Copilot-Unboxed/tools/privacy_validator.py:297**
  - Potential forced registration pattern
  - ```r"must.*sign.*up",```

- **/home/user/ComfyUI-Copilot-Unboxed/tools/privacy_validator.py:298**
  - Potential forced registration pattern
  - ```r"api.*key.*required.*email",```

- **/home/user/ComfyUI-Copilot-Unboxed/tools/privacy_validator.py:299**
  - Potential forced registration pattern
  - ```r"create.*account.*required",```

## 📋 Recommendations

### Critical Actions Required

- Remove all `analytics_call` patterns immediately
- Remove all `email_collection` patterns immediately

### Errors to Fix

- Review and address `api_key_generation` issues
- Review and address `vendor_cdn` issues

### Warnings to Review

- Review flagged items to ensure they are user-controlled
- Update acceptable domains list if needed

---
*Privacy validator for ComfyUI-Copilot-Unboxed*