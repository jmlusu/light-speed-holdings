# Model status report

Generated: 2026-10-26 16:38:27 (local time). Results are a snapshot; free tiers change without notice.

**38 models available**, 32 failing, 46 uncertain, 0 not tested.

## Warnings
- smallModel is 'opencode/gpt-5.1-codex', a PAID OpenCode Zen model (Zen needs billing). Consider a free one, e.g. opencode/big-pickle or opencode/deepseek-v4-flash-free.
- OmniRoute serves 1303 models; 1224 were listed but NOT called (use -Deep to call every one; some upstreams may be paid).
- OpenCode Zen lists 76 paid models (not called): test, claude-fable-5, jev-1.13, claude-fable-5-1, claude-haiku-4-5, claude-haiku-5-5, claude-opus-4-5, claude-opus-4-6, claude-opus-4-7, claude-opus-4-8, claude-opus-5, claude-opus-5-5, ...
- Local models (ollama, llamacpp) were NOT tested. Run with -IncludeLocal to test them.

## Provider health

| Provider | Health | Working | Failing | Uncertain |
|---|---|---|---|---|
| omniroute | UP (15 working) | 15 | 31 | 35 |
| groq-direct | UP (3 working) | 3 | 0 | 0 |
| nvidia-nim-direct | UP (2 working) | 2 | 0 | 0 |
| mistral-direct | UP (2 working) | 2 | 0 | 0 |
| gemini-studio-direct | UP (1 working) | 1 | 0 | 2 |
| cloudflare-direct | UP (11 working) | 11 | 0 | 0 |
| ollama-cloud-direct | UP (4 working) | 4 | 1 | 0 |
| opencode-zen | UNCERTAIN (rate limited / busy) | 0 | 0 | 9 |

## Available now (fastest first)

Model id format is provider/model, as opencode expects.

| Model | Response ms | Note |
|---|---|---|
| groq-direct/qwen/qwen3.8-27b | 699 |  |
| cloudflare-direct/@cf/ibm-granite/granite-4.0-h-micro | 756 |  |
| cloudflare-direct/@cf/meta/llama-3.3-70b-instruct-fp8-fast | 793 |  |
| groq-direct/openai/gpt-oss-20b | 833 |  |
| cloudflare-direct/@cf/mistralai/mistral-small-3.1-24b-instruct | 836 |  |
| mistral-direct/ministral-14b-latest | 920 |  |
| cloudflare-direct/@cf/qwen/qwen2.5-coder-32b-instruct | 923 |  |
| mistral-direct/ministral-8b-latest | 963 |  |
| cloudflare-direct/@cf/meta/llama-4-scout-17b-16e-instruct | 968 |  |
| groq-direct/openai/gpt-oss-120b | 1017 |  |
| cloudflare-direct/@cf/nvidia/nemotron-3-120b-a12b | 1064 |  |
| cloudflare-direct/@cf/meta/llama-3.1-8b-instruct-fp8 | 1102 |  |
| ollama-cloud-direct/gemma4:31b | 1312 |  |
| cloudflare-direct/@cf/openai/gpt-oss-20b | 1324 |  |
| ollama-cloud-direct/gpt-oss:20b | 1468 |  |
| ollama-cloud-direct/gpt-oss:120b | 1492 | empty reply at 64 tokens (reasoning model; usable) |
| nvidia-nim-direct/nvidia/nemotron-3.5-lightning-30b-a3b | 1814 | empty reply at 64 tokens (reasoning model; usable) |
| cloudflare-direct/@cf/google/gemma-4-26b-a4b-it | 1848 |  |
| cloudflare-direct/@cf/qwen/qwen3.8-27b | 1990 |  |
| cloudflare-direct/@cf/qwen/qwen3-30b-a3b-fp8 | 2180 | empty reply at 64 tokens (reasoning model; usable) |
| ollama-cloud-direct/nemotron-3-super | 2532 |  |
| omniroute/auto/coding | 3443 |  |
| omniroute/auto/gemini | 15263 |  |
| omniroute/auto/reasoning:pro | 17160 |  |
| omniroute/auto/coding:pro | 17345 |  |
| omniroute/auto/gemma | 18147 |  |
| gemini-studio-direct/gemma-4-31b-it | 25661 |  |
| omniroute/auto/pro-chat | 25735 |  |
| omniroute/auto/pro-coding | 26491 |  |
| omniroute/auto/best-fast | 28505 |  |
| omniroute/auto/pro-vision | 28574 |  |
| omniroute/auto/best-coding-fast | 28681 |  |
| omniroute/auto/pro-fast | 30100 |  |
| nvidia-nim-direct/openai/gpt-oss-20b | 35180 |  |
| omniroute/auto/fast | 37539 |  |
| omniroute/auto/offline | 42592 |  |
| omniroute/auto/multimodal | 48932 |  |
| omniroute/auto/best-vision | 55664 |  |

## Failing

| Model | Status | HTTP | Note |
|---|---|---|---|
| omniroute/auto | NOT_FOUND | - | in opencode.json but not served by OmniRoute |
| omniroute/oc/x-preview-f-free | NOT_FOUND | - | in opencode.json but not served by OmniRoute |
| ollama-cloud-direct/mistral-large-4 | FORBIDDEN | 403 | This model is currently being rolled out and is not yet available to you. Please check bac... |
| omniroute/auto/best-chaos | ERROR | 200 | 200 but no choices:  |
| omniroute/auto/chaos | ERROR | 200 | 200 but no choices:  |
| omniroute/auto/mimo | BAD_REQUEST | 400 | oc/mimo-v2.5-free: model — [400]: Upstream request failed: Model is unavailable. (HTTP 400... |
| omniroute/oc/north-mini-code-free | BAD_REQUEST | 400 | Model 'north-mini-code-free' is not available in the active live catalog for provider 'ope... |
| omniroute/oc/deepseek-v4-flash-free | BAD_REQUEST | 400 | [400]: Upstream request failed: Model is unavailable. |
| omniroute/opencode/deepseek-v4-flash-free | BAD_REQUEST | 400 | Model 'deepseek-v4-flash-free' is not available in the active live catalog for provider 'o... |
| omniroute/oc/muse-spark-1.2-contributor-free | BAD_REQUEST | 400 | [400]: Upstream request failed: Model is unavailable. |
| omniroute/opencode/muse-spark-1.2-contributor-free | BAD_REQUEST | 400 | Model 'muse-spark-1.2-contributor-free' is not available in the active live catalog for pr... |
| omniroute/oc/mimo-v2.5-free | BAD_REQUEST | 400 | [400]: Upstream request failed: Model is unavailable. |
| omniroute/opencode/mimo-v2.5-free | BAD_REQUEST | 400 | Model 'mimo-v2.5-free' is not available in the active live catalog for provider 'opencode-... |
| omniroute/oc/hy3-free | BAD_REQUEST | 400 | [400]: Upstream request failed: Model is unavailable. |
| omniroute/opencode/hy3-free | BAD_REQUEST | 400 | Model 'hy3-free' is not available in the active live catalog for provider 'opencode-zen'. |
| omniroute/oc/nemotron-3-ultra-free | BAD_REQUEST | 400 | [400]: Upstream request failed: Model is unavailable. |
| omniroute/opencode/nemotron-3-ultra-free | BAD_REQUEST | 400 | Model 'nemotron-3-ultra-free' is not available in the active live catalog for provider 'op... |
| omniroute/oc/laguna-s-2.1-free | BAD_REQUEST | 400 | [400]: Upstream request failed: Model is unavailable. |
| omniroute/opencode/laguna-s-2.1-free | BAD_REQUEST | 400 | Model 'laguna-s-2.1-free' is not available in the active live catalog for provider 'openco... |
| omniroute/opencode-zen/muse-spark-1.2-contributor-free | BAD_REQUEST | 400 | Model 'muse-spark-1.2-contributor-free' is not available in the active live catalog for pr... |
| omniroute/opencode-zen/deepseek-v4-flash-free | BAD_REQUEST | 400 | Model 'deepseek-v4-flash-free' is not available in the active live catalog for provider 'o... |
| omniroute/opencode-zen/mimo-v2.5-free | BAD_REQUEST | 400 | Model 'mimo-v2.5-free' is not available in the active live catalog for provider 'opencode-... |
| omniroute/opencode-zen/hy3-free | BAD_REQUEST | 400 | Model 'hy3-free' is not available in the active live catalog for provider 'opencode-zen'. |
| omniroute/opencode-zen/nemotron-3-ultra-free | BAD_REQUEST | 400 | Model 'nemotron-3-ultra-free' is not available in the active live catalog for provider 'op... |
| omniroute/opencode-zen/laguna-s-2.1-free | BAD_REQUEST | 400 | Model 'laguna-s-2.1-free' is not available in the active live catalog for provider 'openco... |
| omniroute/oc/beam-free | BAD_REQUEST | 400 | Model 'beam-free' is not available in the active live catalog for provider 'opencode'. |
| omniroute/oc/flint-40b-free | BAD_REQUEST | 400 | Model 'flint-40b-free' is not available in the active live catalog for provider 'opencode'... |
| omniroute/oc/mimo-v2.6-flash-free | BAD_REQUEST | 400 | Model 'mimo-v2.6-flash-free' is not available in the active live catalog for provider 'ope... |
| omniroute/oc/nemotron-3.5-super-vl-free | BAD_REQUEST | 400 | Model 'nemotron-3.5-super-vl-free' is not available in the active live catalog for provide... |
| omniroute/oc/jev-1.13-free | BAD_REQUEST | 400 | Model 'jev-1.13-free' is not available in the active live catalog for provider 'opencode'. |
| omniroute/oc/deepseek-v4.1-flash-free | BAD_REQUEST | 400 | Model 'deepseek-v4.1-flash-free' is not available in the active live catalog for provider ... |
| omniroute/oc/glm-5.3-flash-free | BAD_REQUEST | 400 | Model 'glm-5.3-flash-free' is not available in the active live catalog for provider 'openc... |

## Uncertain (retry later; this is not proof they are broken)

| Model | Status | HTTP | Note |
|---|---|---|---|
| gemini-studio-direct/gemma-4-26b-a4b-it | SERVER_ERR | 500 | Internal error encountered. |
| gemini-studio-direct/gemini-3.8-flash | TIMEOUT | 000 | no reply within the time limit |
| omniroute/auto/best-coding | SERVER_ERR | 503 | Maximum combo retry limit reached |
| omniroute/auto/best-reasoning | SERVER_ERR | 503 | Maximum combo retry limit reached |
| omniroute/auto/best-chat | SERVER_ERR | 503 | Maximum combo retry limit reached |
| omniroute/auto/pro-reasoning | SERVER_ERR | 503 | Maximum combo retry limit reached |
| omniroute/auto/chat | SERVER_ERR | 503 | Maximum combo retry limit reached |
| omniroute/auto/cheap | SERVER_ERR | 503 | Maximum combo retry limit reached |
| omniroute/auto/smart | TIMEOUT | 000 | no reply within the time limit |
| omniroute/auto/claude-opus | TIMEOUT | 000 | no reply within the time limit |
| omniroute/auto/claude-sonnet | SERVER_ERR | 503 | Maximum combo retry limit reached |
| omniroute/auto/best-free | TIMEOUT | 000 | no reply within the time limit |
| omniroute/auto/coding:fast | SERVER_ERR | 503 | Maximum combo retry limit reached |
| omniroute/auto/coding:cheap | TIMEOUT | 000 | no reply within the time limit |
| omniroute/auto/coding:free | TIMEOUT | 000 | no reply within the time limit |
| omniroute/auto/coding:reliable | SERVER_ERR | 503 | Maximum combo retry limit reached |
| omniroute/auto/reasoning | TIMEOUT | 000 | no reply within the time limit |
| omniroute/auto/vision | TIMEOUT | 000 | no reply within the time limit |
| omniroute/auto/glm | SERVER_ERR | 504 | zc/glm-5.1: provider — [502]: spawn zcode ENOENT (HTTP 502); dva/glm-5-2-max-1m: provider ... |
| omniroute/auto/minimax | SERVER_ERR | 502 | nvidia/minimaxai/minimax-m3: model — [410]: {"type":"about:blank","title":"Gone","status":... |
| omniroute/auto/zai | TIMEOUT | 000 | no reply within the time limit |
| omniroute/auto/llama | SERVER_ERR | 502 | nvidia/meta/llama-3.2-11b-vision-instruct: auth — [403]: {"status":403,"title":"Forbidden"... |
| omniroute/veoaifree-web/veo | TIMEOUT | 000 | no reply within the time limit |
| omniroute/veoaifree-web/seedance | TIMEOUT | 000 | no reply within the time limit |
| omniroute/veo-free/veo | TIMEOUT | 000 | no reply within the time limit |
| omniroute/veo-free/seedance | TIMEOUT | 000 | no reply within the time limit |
| omniroute/opencode-zen/big-pickle | RATE_LIMIT | 429 | All credentials for model big-pickle are cooling down |
| omniroute/opencode-zen/beam-free | RATE_LIMIT | 429 | All credentials for model beam-free are cooling down |
| omniroute/opencode-zen/flint-40b-free | RATE_LIMIT | 429 | All credentials for model flint-40b-free are cooling down |
| omniroute/opencode-zen/mimo-v2.6-flash-free | RATE_LIMIT | 429 | All credentials for model mimo-v2.6-flash-free are cooling down |
| omniroute/opencode-zen/nemotron-3.5-super-vl-free | RATE_LIMIT | 429 | All credentials for model nemotron-3.5-super-vl-free are cooling down |
| omniroute/opencode-zen/nemotron-3.5-lightning-free | RATE_LIMIT | 429 | All credentials for model nemotron-3.5-lightning-free are cooling down |
| omniroute/opencode-zen/jev-1.13-free | RATE_LIMIT | 429 | All credentials for model jev-1.13-free are cooling down |
| omniroute/opencode-zen/deepseek-v4.1-flash-free | RATE_LIMIT | 429 | All credentials for model deepseek-v4.1-flash-free are cooling down |
| omniroute/opencode-zen/glm-5.3-flash-free | RATE_LIMIT | 429 | All credentials for model glm-5.3-flash-free are cooling down |
| omniroute/oc/big-pickle | RATE_LIMIT | 429 | [429]: Free usage limit reached. Free models work in OpenCode (https://opencode.ai); subsc... |
| omniroute/oc/nemotron-3.5-lightning-free | RATE_LIMIT | 429 | [429]: Free usage limit reached. Free models work in OpenCode (https://opencode.ai); subsc... |
| opencode-zen/big-pickle | RATE_LIMIT | 429 | Free usage limit reached. Free models work in OpenCode (https://opencode.ai); subscribe to... |
| opencode-zen/beam-free | RATE_LIMIT | 429 | Free usage limit reached. Free models work in OpenCode (https://opencode.ai); subscribe to... |
| opencode-zen/flint-40b-free | RATE_LIMIT | 429 | Free usage limit reached. Free models work in OpenCode (https://opencode.ai); subscribe to... |
| opencode-zen/mimo-v2.6-flash-free | RATE_LIMIT | 429 | Free usage limit reached. Free models work in OpenCode (https://opencode.ai); subscribe to... |
| opencode-zen/nemotron-3.5-super-vl-free | RATE_LIMIT | 429 | Free usage limit reached. Free models work in OpenCode (https://opencode.ai); subscribe to... |
| opencode-zen/nemotron-3.5-lightning-free | RATE_LIMIT | 429 | Free usage limit reached. Free models work in OpenCode (https://opencode.ai); subscribe to... |
| opencode-zen/jev-1.13-free | RATE_LIMIT | 429 | Free usage limit reached. Free models work in OpenCode (https://opencode.ai); subscribe to... |
| opencode-zen/deepseek-v4.1-flash-free | RATE_LIMIT | 429 | Free usage limit reached. Free models work in OpenCode (https://opencode.ai); subscribe to... |
| opencode-zen/glm-5.3-flash-free | RATE_LIMIT | 429 | Free usage limit reached. Free models work in OpenCode (https://opencode.ai); subscribe to... |
