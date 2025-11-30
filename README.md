[中文](./README_CN.md) ｜ English

<div align="center">

# 🎯 ComfyUI-Copilot-Unboxed

**The unboxed version - bring your own AI**

*Privacy-focused community fork of [AIDC-AI/ComfyUI-Copilot](https://github.com/AIDC-AI/ComfyUI-Copilot)*

<h4 align="center">

<div align="center">
<img src="https://img.shields.io/badge/Version-2.0.0--unboxed-blue.svg" alt="Version">
<img src="https://img.shields.io/github/stars/DataSparBrian/ComfyUI-Copilot-Unboxed?color=yellow" alt="Stars">
<img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
<img src="https://img.shields.io/badge/Privacy-Focused-brightgreen.svg" alt="Privacy">

</h4>

**Tagline**: *"The unboxed version - bring your own AI"*

</div>

</div>

---

## 🙏 About This Fork

This fork builds upon the **excellent work** of the [original ComfyUI-Copilot team at Alibaba International Digital Commerce (AIDC-AI)](https://github.com/AIDC-AI/ComfyUI-Copilot). We've "unboxed" their great tool to remove vendor lock-in while preserving all the powerful workflow automation features.

### 🌟 Credits to Original Developers

**Massive thanks to AIDC-AI** for creating this powerful ComfyUI assistant! The core technology, workflow generation, debugging system, and agent architecture are their brilliant work. This fork simply makes it vendor-neutral.

- **Original Repository**: https://github.com/AIDC-AI/ComfyUI-Copilot
- **Original Authors**: Alibaba International Digital Commerce (AIDC-AI)
- **Original License**: MIT
- **Research Paper**: [ACL 2025](https://aclanthology.org/2025.acl-demo.61.pdf)

---

## 🎁 What "Unboxed" Means

**Unboxed = Freed from vendor packaging, ready for your own AI services.**

This fork:
- ✅ **DOES** maintain full internet connectivity for user-specified APIs
- ✅ **DOES** support OpenAI, Anthropic, OpenRouter, and other external services
- ✅ **DOES** work with self-hosted LLMs via API calls
- ✅ **DOES** preserve all core ComfyUI-Copilot functionality
- ❌ Does **NOT** phone home to vendor servers
- ❌ Does **NOT** collect telemetry or analytics
- ❌ Does **NOT** require vendor cloud service registration
- ❌ Does **NOT** show promotional popups

**Philosophy**: We respect the original developers' excellent work at AIDC-AI. This fork simply "unboxes" their tool so users can bring their own AI services without vendor lock-in.

---

## 📊 What We Changed

### ✅ **Added:**
- **BYOK (Bring Your Own Key)** support for any OpenAI-compatible API
- Support for **OpenRouter**, **Anthropic Claude**, and other providers
- Clean configuration UI for **self-hosted LLMs** (Ollama, LM Studio, etc.)
- **Privacy-focused operation** with no telemetry
- **Automated upstream tracking** for easy integration of upstream improvements
- Comprehensive documentation for long-term maintainability

### ❌ **Removed:**
- Vendor cloud service registration requirements
- Email collection and forced API key signup
- Analytics and telemetry tracking
- Promotional popups and QR codes
- Privacy policy links to vendor CDN

### 🎯 **Unchanged:**
- All core workflow generation, debugging, and rewriting features ✅
- Node recommendation and query systems ✅
- Parameter tuning capabilities ✅
- Model download functionality ✅
- Full internet connectivity for **YOUR** AI services ✅

---

## 🔥 Core Features (V2.0.0)

All features from the original ComfyUI-Copilot are preserved:

- 1. 💎 **Generate First Version Workflow**: Based on your text description, generate workflows tailored to your needs.
- 2. 💎 **Workflow Debug**: Automatically analyze errors, fix parameter errors and workflow connection issues.
- 3. 💎 **Workflow Rewriting**: Modify workflows based on your description - adjust parameters, add nodes, improve logic.
- 4. 💎 **Parameter Tuning**: Batch execute different parameter combinations and generate visual comparison results.
- 5. 💎 **Node Recommendations**: Get node recommendations based on your description with explanations.
- 6. 💎 **Node Query System**: Explore nodes in depth, view descriptions, parameters, and usage tips.
- 7. 💎 **Model Recommendations**: Find base models and LoRAs based on your requirements.
- 8. 💎 **Downstream Node Recommendations**: Get subgraph recommendations based on existing nodes.

---

## 🚀 Getting Started

### Installation

1. Clone **this fork** (not the original repository):

   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/DataSparBrian/ComfyUI-Copilot-Unboxed.git
   cd ComfyUI-Copilot-Unboxed
   pip install -r requirements.txt
   ```

   For Windows users:
   ```bash
   python_embeded\python.exe -m pip install -r ComfyUI\custom_nodes\ComfyUI-Copilot-Unboxed\requirements.txt
   ```

2. **Using ComfyUI Manager**: Search for "ComfyUI-Copilot-Unboxed" in Custom Nodes Manager.
   - Note: The original "ComfyUI-Copilot" in the manager is the upstream version with vendor registration

### Activation

After running ComfyUI, find the Copilot activation button on the left side of the panel.

### Configuration

Click the ⚙️ button to configure your AI provider:

#### **For OpenRouter** (Recommended for flexibility):
- API Endpoint: `https://openrouter.ai/api/v1`
- API Key: Your OpenRouter key (from https://openrouter.ai/keys)
- Model: `anthropic/claude-sonnet-4` or `openai/gpt-4`

#### **For Ollama** (Local, private):
- API Endpoint: `http://localhost:11434/v1`
- API Key: (leave empty)
- Model: `qwen2.5:7b` or `llama3.1:8b`

#### **For LM Studio** (Local, private):
- API Endpoint: `http://localhost:1234/v1`
- API Key: (leave empty)
- Model: Select from loaded models

#### **For OpenAI**:
- API Endpoint: `https://api.openai.com/v1`
- API Key: Your OpenAI key
- Model: `gpt-4o` or `gpt-4-turbo`

#### **For Anthropic Claude**:
- API Endpoint: `https://api.anthropic.com/v1`
- API Key: Your Anthropic key
- Model: `claude-sonnet-4`

#### **For Custom/Self-Hosted**:
- API Endpoint: Any OpenAI-compatible server URL
- API Key: Your API key (if required)
- Model: Supported model name

---

## 🔧 Advanced: Workflow LLM Configuration

For workflow debugging and modification, you can optionally configure a separate, more powerful LLM:

- **Recommended**: Claude Sonnet 4 or GPT-4 (requires long context)
- **Minimum**: 8192 token context window
- **Note**: If not set, uses the default model provided by the fork

---

## 🛠️ Troubleshooting

### "API key is required" error
- Make sure you've configured your API endpoint and key in the settings
- For local LLMs (Ollama, LM Studio), ensure the server is running

### Workflow generation fails
- Check that your selected model supports the required context length
- Try a more capable model (Claude Sonnet 4, GPT-4)
- Ensure your API key has sufficient credits/quota

### Models not loading
- For ModelScope downloads: This is optional, models can be downloaded manually
- Check your internet connection for external API calls

---

## 🤝 Contributing

We welcome contributions! This fork aims to:
1. **Stay synchronized** with upstream AIDC-AI/ComfyUI-Copilot improvements
2. **Maintain privacy focus** - no telemetry, no vendor lock-in
3. **Preserve excellent features** built by the original team

### Reporting Issues

- For **privacy concerns**: Open an issue in this repository
- For **core functionality bugs**: Consider reporting to [upstream](https://github.com/AIDC-AI/ComfyUI-Copilot/issues) (helps everyone!)
- For **fork-specific issues**: Use [our GitHub Issues](https://github.com/DataSparBrian/ComfyUI-Copilot-Unboxed/issues)

---

## 🔄 Upstream Sync

This fork maintains synchronization with upstream improvements:

- **Upstream Repository**: https://github.com/AIDC-AI/ComfyUI-Copilot
- **Sync Strategy**: Weekly automated checks for new features and bug fixes
- **Merge Policy**: Accept all improvements except telemetry/vendor lock-in
- **Automation**: See `tools/` directory for upstream monitoring scripts

We actively merge improvements from AIDC-AI while blocking only privacy-invasive changes.

---

## 📚 Documentation

- **For Users**: This README + [LM Studio Setup Guide](./LMSTUDIO_SETUP.md)
- **For Developers**: See `docs/maintenance/` for fork architecture and upstream sync strategy
- **Original Docs**: Visit [AIDC-AI/ComfyUI-Copilot](https://github.com/AIDC-AI/ComfyUI-Copilot) for detailed feature documentation

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/DataSparBrian/ComfyUI-Copilot-Unboxed/issues)
- **Discussions**: [GitHub Discussions](https://github.com/DataSparBrian/ComfyUI-Copilot-Unboxed/discussions)
- **Fork Maintainer**: [@DataSparBrian](https://github.com/DataSparBrian)

**For the original project**, visit:
- Original repository: https://github.com/AIDC-AI/ComfyUI-Copilot
- Original team contact: ComfyUI-Copilot@service.alibaba.com
- Discord: https://discord.gg/rb36gWG9Se

---

## 📄 License

This project is licensed under the **MIT License** - same as the original.

### Copyright Notice

- **Original Work**: Copyright (C) 2025 AIDC-AI (Alibaba International Digital Commerce)
- **Fork Modifications**: Copyright (C) 2025 DataSparBrian
- **License**: MIT License - see [LICENSE](https://opensource.org/licenses/MIT)

---

## 🌟 Acknowledgments

### Original Developers

**This fork would not exist without the exceptional work of the AIDC-AI team.** Their research, architecture, and implementation of the ComfyUI-Copilot agent system is truly impressive. We are grateful for their contribution to the open-source community.

### Why Fork?

We created this fork not to compete with AIDC-AI, but to provide an option for users who:
- Want to use their own AI services (OpenRouter, self-hosted, etc.)
- Prefer privacy-focused tools without telemetry
- Need vendor-neutral solutions for their workflows
- Value the excellent features AIDC-AI built, vendor-free

### Original Project Recognition

Please support the original AIDC-AI/ComfyUI-Copilot project:
- ⭐ Star the [original repository](https://github.com/AIDC-AI/ComfyUI-Copilot)
- 📖 Read their [research paper](https://aclanthology.org/2025.acl-demo.61.pdf)
- 🤝 Contribute bug fixes back to upstream when possible

---

## 🎯 Philosophy

**"Unbox the tool, keep the excellence"**

We believe great software should be:
- **Privacy-respecting**: No telemetry, no tracking
- **Vendor-neutral**: Bring your own AI services
- **Community-driven**: Open development, respectful of original creators
- **Feature-complete**: All functionality preserved

This fork embodies these values while honoring the brilliant work of AIDC-AI.

---

**Thank you to AIDC-AI for creating ComfyUI-Copilot, and thank you for choosing the Unboxed version!** 🎉
