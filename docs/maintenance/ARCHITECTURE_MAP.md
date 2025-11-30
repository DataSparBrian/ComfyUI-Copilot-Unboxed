# ComfyUI-Copilot-Unboxed Architecture Map

> **Last Updated**: 2025-11-30
> **Fork**: https://github.com/DataSparBrian/ComfyUI-Copilot-Unboxed
> **Upstream**: https://github.com/AIDC-AI/ComfyUI-Copilot

This document provides a comprehensive classification of all files in the codebase, categorizing them by functionality and modification status for the privacy-focused fork.

## File Classification Legend

- **✅ KEEP SYNCED**: Core functionality - merge upstream changes freely
- **⚠️ MODIFIED**: Privacy modifications applied - review upstream changes carefully
- **❌ REMOVED**: Vendor lock-in code - block from upstream
- **📝 FORK-SPECIFIC**: Documentation/config specific to this fork

---

## Frontend (UI)

### Core UI Components (✅ KEEP SYNCED)

```
ui/src/components/
├── debug/                           # Debug interface components
│   ├── ParameterDebugInterfaceNew.tsx
│   ├── screens/
│   └── utils/
├── ui/                              # Reusable UI components
│   ├── Button.tsx
│   ├── Card.tsx
│   ├── CollapsibleCard.tsx
│   ├── Input.tsx
│   ├── Loading-icon.tsx
│   ├── Modal.tsx
│   ├── Markdown.tsx
│   ├── RestoreCheckpoint.tsx
│   ├── StartLink.tsx
│   └── TabButton.tsx
└── workflowChat/                    # Main chat interface
    └── workflowChat.tsx
```

**Strategy**: These are core UI components. Merge upstream improvements freely after privacy validation.

### Modified UI Components (⚠️ MODIFIED)

```
ui/src/components/chat/
├── ApiKeyModal.tsx                  # MODIFIED: Email collection removed, BYOK-focused
├── ChatInput.tsx                    # Review for vendor-specific features
├── ModelDownloadModal.tsx           # Review for vendor integrations
└── messages/                        # Message display components
    ├── WorkflowOption.tsx
    ├── ModelOption.tsx
    ├── NodeSearch.tsx
    ├── DownstreamSubgraphs.tsx
    └── DebugGuide.tsx
```

**Key Modifications**:
- `ApiKeyModal.tsx:246-270`: Removed `handleSendEmail` function (vendor registration)
- `ApiKeyModal.tsx:336-382`: Removed email collection UI and privacy policy links
- `ApiKeyModal.tsx:366,374`: Removed Alibaba CDN privacy policy/terms links

**Strategy**: Review upstream changes to these files carefully. Re-apply privacy modifications if overwritten.

### Configuration Files (⚠️ MODIFIED)

```
ui/src/
├── config.ts                        # MODIFIED: API base URL configuration
└── const.ts                         # Check for vendor-specific constants
```

**Key Modifications**:
- `config.ts:8`: github_url updated to fork URL
- May contain vendor endpoints that need to be neutralized

**Strategy**: Keep local modifications, merge non-endpoint changes from upstream.

### Utility Files (✅ KEEP SYNCED with validation)

```
ui/src/utils/
├── civitUtils.ts                    # CivitAI integration (external service - acceptable)
├── queuePrompt.ts
├── tools.ts
├── downloadJsonFile.ts
├── deepJsonDiffCheck.ts
├── graphUtils.ts
├── localStorageManager.ts
├── downloadWorkflowsZip.ts
├── encryptUtils.ts
├── findSfwImage.ts
├── uuid.ts
├── mediaMetadataUtils.ts
├── showAlert.ts
├── jsonUtils.ts
├── indexedDB.ts
├── comfyuiWorkflowApi2Ui.ts
├── crypto.ts                        # RSA key fetching - check vendor endpoints
├── comfyapp.ts
├── saveShareKey.ts
├── privacyUtils.ts                  # Ironic - check for actual privacy code
└── OsPathUtils.ts
```

**Files needing special attention**:
- `crypto.ts`: Check `fetchRsaPublicKey()` - may call vendor endpoints
- `privacyUtils.ts`: Verify actual privacy-related code vs vendor terms
- `civitUtils.ts`: External service calls (CivitAI) - user choice, acceptable

**Strategy**: Merge freely but scan for new network calls to vendor endpoints.

### API Client Files (⚠️ REVIEW CAREFULLY)

```
ui/src/apis/
├── workflowChatApi.ts               # Main API client - check for vendor endpoints
├── comfyApiCustom.ts                # ComfyUI API wrapper
└── rewriteExpertApi.ts              # Workflow rewrite API
```

**Strategy**: Scan for any non-local API calls. All endpoints should be local ComfyUI server or user-specified.

---

## Backend (Python)

### Core Functionality (✅ KEEP SYNCED)

```
backend/
├── core.py                          # Core plugin logic
├── agent_factory.py                 # Agent creation logic
├── service/                         # Business logic
│   ├── workflow_rewrite_tools.py
│   ├── mcp_client.py               # MCP client for agent communication
│   ├── message_memory.py
│   ├── parameter_tools.py
│   ├── workflow_rewrite_agent_simple.py
│   ├── workflow_rewrite_agent.py
│   ├── summary_agent.py
│   ├── debug_agent.py
│   └── link_agent_tools.py
└── dao/                            # Database access
    ├── expert_table.py
    ├── session_message_table.py
    └── workflow_table.py
```

**Strategy**: Core business logic. Merge upstream improvements freely after privacy scan.

### Controllers/APIs (⚠️ REVIEW CAREFULLY)

```
backend/controller/
├── conversation_api.py              # Main chat API - review for vendor calls
├── llm_api.py                       # LLM configuration API - already BYOK-friendly
└── expert_api.py                    # Expert knowledge API
```

**Findings**:
- `conversation_api.py`: All endpoints are local - ✅ Good
- `llm_api.py`: Already supports OpenAI and LMStudio - ✅ Good
- No vendor API calls found in controllers

**Strategy**: Merge upstream changes but validate no new vendor endpoints are introduced.

### Utilities (⚠️ MIXED)

```
backend/utils/
├── comfy_gateway.py                 # ComfyUI gateway - local only
├── request_context.py               # Request context management
├── modelscope_gateway.py            # ModelScope API - Chinese model hub
├── auth_utils.py                    # API key extraction - repurposed for user keys
├── globals.py                       # Global state
├── key_utils.py                     # Key utilities
├── logger.py                        # Logging
├── string_utils.py                  # String utilities
└── track_utils.py                   # ❌ REMOVED: Was empty, likely for telemetry
```

**Key files**:
- `track_utils.py`: Empty file - likely placeholder for telemetry. Mark for removal.
- `modelscope_gateway.py`: Downloads from ModelScope (Chinese model hub) - user choice, acceptable
- `auth_utils.py`: Extracts API keys from headers - repurposed for user's own keys

**Strategy**:
- Remove `track_utils.py` completely
- Keep ModelScope integration (user choice for model downloads)
- Merge other utils freely

---

## Static Assets & Configuration

### Public Assets (⚠️ VENDOR CONTENT)

```
public/
├── showcase/
│   ├── showcase.json                # Contains Alibaba OSS image URLs
│   └── showcase_en.json             # Contains Alibaba OSS image URLs
```

**Vendor content identified**:
- Both files contain images hosted on `aib-vision-hz.oss-accelerate.aliyuncs.com`
- QR codes and WeChat promotional content

**Strategy**: Replace with local examples or generic placeholders. Remove QR codes.

### Distribution Files (🔄 AUTO-GENERATED)

```
dist/copilot_web/                    # Built frontend files
├── workflowChat-Bs515Oed.js
├── vendor-markdown-B4Av9P7l.js
├── message-components--sDgdV1o.js
├── input.js
├── DebugGuide-CqaaNx4k.js
└── WorkflowOption-CUEyiK7N.js
```

**Strategy**: These are built files. Will be regenerated after source modifications.

### Entry Points (✅ KEEP SYNCED)

```
entry/
├── entry.js                         # Main entry point
└── comfyui-bridge.js                # ComfyUI integration bridge
```

**Strategy**: Core integration code. Merge upstream freely.

---

## Documentation (📝 FORK-SPECIFIC)

### Current Documentation (⚠️ NEEDS FORK UPDATE)

```
./
├── README.md                        # ⚠️ NEEDS REPLACEMENT with fork info
├── README_CN.md                     # Chinese README - needs fork update
├── HOW_TO_USE_LMSTUDIO.md          # ✅ Useful, keep and enhance
├── LMSTUDIO_IMPLEMENTATION.md       # ✅ Useful, keep
├── LMSTUDIO_SETUP.md                # ✅ Useful, keep
├── LICENSE                          # MIT - keep same
├── NOTICE.txt                       # Attribution - keep
└── Authors.txt                      # Original authors - keep and add fork maintainer
```

**Strategy**:
- Replace README with fork-specific version (attribution to original!)
- Keep LMStudio docs (already BYOK-focused)
- Add `docs/maintenance/` directory (fork-specific)

### New Fork Documentation (📝 FORK-SPECIFIC)

```
docs/
└── maintenance/                     # New directory for fork maintenance
    ├── ARCHITECTURE_MAP.md          # This file
    ├── MODIFICATION_MANIFEST.json   # Change tracking
    ├── UPSTREAM_SYNC_STRATEGY.md    # Sync process documentation
    └── PRIVACY_AUDIT_CHECKLIST.md   # Privacy validation checklist (future)
```

---

## Build & Development Files (✅ KEEP SYNCED)

```
./
├── package-lock.json
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Python project config
├── .gitignore
└── .cursorignore
```

**Strategy**: Merge upstream dependency updates after security review.

---

## Root Files

### Plugin Registration (✅ KEEP SYNCED)

```
./
├── __init__.py                      # ComfyUI plugin entry point
└── index.html                       # Frontend HTML
└── poster.html                      # Poster/preview HTML
```

**Strategy**: Core plugin files. Merge upstream changes freely.

---

## Summary by Modification Type

### Files to Remove Completely (❌)

1. `backend/utils/track_utils.py` - Empty telemetry placeholder

### Files with Privacy Modifications (⚠️)

1. `ui/src/components/chat/ApiKeyModal.tsx` - Email collection removed
2. `ui/src/config.ts` - GitHub URL updated
3. `public/showcase/showcase.json` - OSS URLs need replacement
4. `public/showcase/showcase_en.json` - OSS URLs need replacement
5. `README.md` - Fork information and attribution
6. `README_CN.md` - Fork information (Chinese)

### Vendor Content to Replace (🔄)

1. Privacy policy links in `ApiKeyModal.tsx`
2. Alibaba OSS image URLs in showcase files
3. WeChat/Discord promotional links in README

### Files That Are Already BYOK-Friendly (✅)

1. `backend/controller/llm_api.py` - Already supports custom endpoints!
2. `backend/controller/conversation_api.py` - Uses header-based LLM config
3. `ui/src/components/chat/ApiKeyModal.tsx` - Has OpenAI/LMStudio support (just needs email removal)

---

## Network Call Inventory

### User-Controlled External Services (✅ Acceptable)

| Service | File | Purpose | User Control |
|---------|------|---------|--------------|
| OpenAI API | Various | LLM inference | User provides API key |
| LMStudio | Various | Local LLM inference | User runs locally |
| CivitAI | `civitUtils.ts` | Model browsing | User choice |
| ModelScope | `modelscope_gateway.py` | Model downloads | User choice |
| Custom endpoints | Various | User's own APIs | User configures |

### Vendor Endpoints to Remove (❌)

| Endpoint | File | Purpose | Action |
|----------|------|---------|--------|
| `/api/user/create` | `ApiKeyModal.tsx:251` | Email collection | ❌ Remove |
| Alibaba CDN privacy policy | `ApiKeyModal.tsx:366` | Terms link | ❌ Remove |
| Alibaba CDN terms | `ApiKeyModal.tsx:374` | Terms link | ❌ Remove |
| Alibaba OSS images | `public/showcase/*.json` | Showcase images | 🔄 Replace |

### Local ComfyUI Endpoints (✅ Keep)

All endpoints in `backend/controller/` are local ComfyUI server endpoints - these are fine!

---

## Merge Strategy by Directory

| Directory | Strategy | Risk Level | Review Process |
|-----------|----------|------------|----------------|
| `backend/service/` | Auto-merge after scan | Low | Automated privacy scan |
| `backend/controller/` | Review carefully | Medium | Manual review of new endpoints |
| `backend/utils/` | Merge most, block track_utils | Low | Automated + manual |
| `ui/src/components/ui/` | Auto-merge after scan | Low | Automated scan |
| `ui/src/components/chat/` | Review carefully | High | Manual review required |
| `ui/src/components/debug/` | Auto-merge after scan | Low | Automated scan |
| `ui/src/utils/` | Review network calls | Medium | Automated scan + manual |
| `ui/src/apis/` | Review carefully | High | Manual review of all changes |
| `public/` | Manual review | High | Check for vendor content |
| Root config files | Review | Medium | Check for vendor URLs |

---

## Upstream Tracking Notes

**Upstream Repository**: `https://github.com/AIDC-AI/ComfyUI-Copilot`
**Upstream Branch**: `main`
**Last Upstream Sync**: (TBD - will be tracked in MODIFICATION_MANIFEST.json)

**High-Value Upstream Changes to Merge**:
- Bug fixes in agent logic
- New workflow features
- Performance improvements
- UI enhancements (non-promotional)
- New node support
- ComfyUI compatibility updates

**Upstream Changes to Block**:
- New telemetry/analytics code
- New vendor registration requirements
- Promotional content
- Vendor cloud service integrations

---

## Maintenance Checklist

When syncing from upstream:

1. ✅ Run `tools/upstream_monitor.py --check`
2. ✅ Review categorized changes
3. ✅ Run `tools/privacy_validator.py --scan`
4. ✅ Check this ARCHITECTURE_MAP for file classification
5. ✅ Manually review high-risk files (APIs, chat components)
6. ✅ Apply changes with `tools/apply_upstream_changes.py`
7. ✅ Re-run privacy validator
8. ✅ Update MODIFICATION_MANIFEST.json
9. ✅ Test all BYOK functionality
10. ✅ Commit with descriptive message acknowledging upstream work

---

## Credits

**Original Developers**: Alibaba International Digital Commerce (AIDC-AI)
**Original Repository**: https://github.com/AIDC-AI/ComfyUI-Copilot
**Fork Purpose**: Privacy-focused, vendor-neutral version maintaining full functionality
**Fork Philosophy**: Respectfully removing vendor lock-in while preserving excellent core features
