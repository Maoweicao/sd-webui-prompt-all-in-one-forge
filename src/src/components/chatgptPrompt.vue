<template>
    <Transition name="fadeDown">
        <div class="physton-chatgpt-prompt" v-if="isOpen" @click="close">
        <div class="chatgpt-main" @click.stop>
            <div class="chatgpt-close" @click="close">
                <icon-svg name="close"/>
            </div>
            <div class="chatgpt-body" @click.stop>
                <div :class="['body-panel', hidePanels['api'] ? 'fold': '']">
                    <div class="panel-header">
                        <div class="panel-unfold" @click="onUnfoldClick('api')">
                            <icon-svg class="hover-scale-120" name="unfold"/>
                        </div>
                        <div class="panel-title">{{ getLang('api_config') }}</div>
                    </div>
                    <div class="panel-content">
                        <div class="body-line">
                            <div class="line-title">{{ getLang('api_provider') }}</div>
                            <div class="line-content">
                                <select v-model="selectedApi" @change="onApiChange">
                                    <option value="openai">OpenAI / ChatGPT</option>
                                    <option value="deepseek">Deepseek</option>
                                    <option value="cherryin">CherryIn</option>
                                    <option value="siliconflow">硅基流动 SiliconFlow</option>
                                </select>
                            </div>
                        </div>
                        <div class="body-line" v-for="config in configs">
                            <div class="line-title">{{ config.title_key ? getLang(config.title_key) : config.title }}</div>
                            <div class="line-content">
                                <input type="text" v-if="config.type == 'input'" v-model="config.value">
                                <select v-if="config.type == 'select'" v-model="config.value">
                                    <option v-for="option in config.options" :value="option">{{ option }}</option>
                                </select>
                                <div v-if="config.type == 'select_or_input'" class="select-or-input-container">
                                    <select v-model="config.selectValue" @change="onSelectChange(config)">
                                        <option value="">自定义输入...</option>
                                        <option v-for="option in config.options" :value="option">{{ option }}</option>
                                    </select>
                                    <input type="text" v-model="config.value" @change="onChangeConfigValue(config)" :placeholder="'自定义模型名称'">
                                </div>
                                <div v-if="config.desc" v-html="config.desc"></div>
                            </div>
                        </div>
                        <div class="body-line">
                            <div class="line-title"></div>
                            <div class="line-content text-right">
                                <div class="common-btn hover-scale-120" @click="onGetModelsClick" style="margin-right: 10px;">
                                    <icon-svg v-if="getModelsIng" name="loading"/>
                                    <template v-else>{{ getLang('get_models') }}</template>
                                </div>
                                <div class="common-btn hover-scale-120" @click="onSaveConfigClick">
                                    <icon-svg v-if="saveConfigIng" name="loading"/>
                                    <template v-else>{{ getLang('save') }}</template>
                                </div>
                            </div>
                        </div>
                        <div class="body-line" v-if="models.length > 0">
                            <div class="line-title">{{ getLang('available_models') }}</div>
                            <div class="line-content">
                                <div class="models-container">
                                    <div v-for="model in models" :key="model.id" class="model-item" @click="onModelSelect(model.id)">
                                        <div class="model-name">{{ model.id }}</div>
                                        <div class="model-owned-by" v-if="model.owned_by">{{ model.owned_by }}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div :class="['body-panel', hidePanels['send'] ? 'fold': '']">
                    <div class="panel-header">
                        <div class="panel-unfold" @click="onUnfoldClick('send')">
                            <icon-svg class="hover-scale-120" name="unfold"/>
                        </div>
                        <div class="panel-title">{{ getLang('image_desc') }}</div>
                    </div>
                    <div class="panel-content">
                        <div class="body-line">
                            <div class="line-title">{{ getLang('preset') }}
                                <div class="line-subtitle">{{ getLang('ai_one') }}</div>
                            </div>
                            <div class="line-content">
                                <textarea :value="chatPreset" @change="onPresetChange" style="height: 100px"></textarea>
                            </div>
                        </div>
                        <div class="body-line">
                            <div class="line-title"></div>
                            <div class="line-content text-right">
                                <a href="javascript:" @click="onRestoreClick">{{ getLang('restore_to_default') }}</a>
                            </div>
                        </div>
                        <div class="body-line">
                            <div class="line-title">{{ getLang('image_desc') }}
                                <div class="line-subtitle">{{ getLang('ai_two') }}</div>
                            </div>
                            <div class="line-content">
                                <textarea style="height: 100px" ref="imageDesc" v-model="imageDesc"
                                          :placeholder="getLang('input_image_desc')"></textarea>
                            </div>
                        </div>
                        <div class="body-line">
                            <div class="line-title"></div>
                            <div class="line-content text-right">
                                <div class="common-btn hover-scale-120" @click="onGenClick">
                                    <icon-svg v-if="genIng" name="loading"/>
                                    <template v-else>{{ getLang('generate') }}</template>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div :class="['body-panel', hidePanels['result'] ? 'fold': '']">
                    <div class="panel-header">
                        <div class="panel-unfold" @click="onUnfoldClick('result')">
                            <icon-svg class="hover-scale-120" name="unfold"/>
                        </div>
                        <div class="panel-title">{{ getLang('generate_result') }}</div>
                    </div>
                    <div class="panel-content">
                        <div class="body-line">
                            <div class="line-title">{{ getLang('generate_result') }}</div>
                            <div class="line-content">
                                <textarea style="height: 100px" v-model="promptResult"></textarea>
                            </div>
                        </div>
                        <div class="body-line" v-if="promptResult">
                            <div class="line-title"></div>
                            <div class="line-content text-right">
                                <div class="common-btn hover-scale-120" @click="onUseClick">{{ getLang('use') }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </Transition>
</template>
<script>
import LanguageMixin from "@/mixins/languageMixin";
import IconSvg from "@/components/iconSvg.vue";
import common from "@/utils/common";

export default {
    name: 'ChatgptPrompt',
    components: {IconSvg},
    mixins: [LanguageMixin],
    props: {},
    data() {
        return {
            isOpen: false,
            api: {},
            configs: [],
            chatPreset: '',
            hidePanels: {
                api: true,
            },
            imageDesc: '',
            promptResult: '',
            saveConfigIng: false,
            genIng: false,
            selectedApi: 'openai',
            apiConfigs: {},
            getModelsIng: false,
            models: [],
        }
    },
    emits: ['use'],
    computed: {},
    mounted() {
    },
    methods: {
        open() {
            this.isOpen = true
            this.saveConfigIng = false
            this.genIng = false

            this.gradioAPI.getDatas(['chatgpt_prompts_preset', 'chatgpt_key', 'chatgpt_selected_api']).then(res => {
                console.log(res)
                if (res.chatgpt_prompts_preset !== null) {
                    this.chatPreset = res.chatgpt_prompts_preset
                } else {
                    this.chatPreset = this.getLang('chatgpt_prompts_preset')
                }

                // 设置选中的API
                if (res.chatgpt_selected_api) {
                    this.selectedApi = res.chatgpt_selected_api
                }

                // 获取所有API的配置
                this.apiConfigs = {}
                if (res.chatgpt_key && typeof res.chatgpt_key === 'object') {
                    this.apiConfigs = res.chatgpt_key
                }

                // 加载当前选中API的配置
                this.loadApiConfig(this.selectedApi)
            })
        },
        close() {
            this.isOpen = false
        },
        onApiChange() {
            this.loadApiConfig(this.selectedApi)
            // 保存选中的API
            this.gradioAPI.setData('chatgpt_selected_api', this.selectedApi)
        },
        loadApiConfig(apiKey) {
            this.configs = []
            let configs = {}
            let api = common.getTranslateApiItem(this.translateApis, apiKey)
            if (!api) {
                console.error('API not found:', apiKey)
                return
            }
            api = JSON.parse(JSON.stringify(api))
            
            // 获取该API的配置
            if (this.apiConfigs[apiKey]) {
                configs = this.apiConfigs[apiKey]
            } else {
                for (const item of api.config) {
                    configs[item.key] = item.default || ''
                }
            }
            
            if (!configs['api_key']) {
                this.hidePanels['api'] = false
            }
            
            for (const item of api.config) {
                item.value = configs[item.key]
                // 为 select_or_input 类型添加 selectValue 属性
                if (item.type === 'select_or_input') {
                    // 检查当前值是否在选项中
                    if (item.options && item.options.includes(item.value)) {
                        item.selectValue = item.value
                    } else {
                        item.selectValue = ''
                    }
                }
                this.configs.push(item)
            }
        },
        onChangeConfigValue(config) {
            if (config.type === 'input' && config.value === '' && config.default) {
                config.value = config.default
            }
        },
        onSelectChange(config) {
            // 当选择了预定义选项时，更新输入框的值
            if (config.selectValue) {
                config.value = config.selectValue
            }
            this.onChangeConfigValue(config)
        },
        onGetModelsClick() {
            if (this.getModelsIng) return
            
            // 检查是否有必要的配置
            const apiBaseConfig = this.configs.find(c => c.key === 'api_base')
            const apiKeyConfig = this.configs.find(c => c.key === 'api_key')
            
            if (!apiBaseConfig || !apiBaseConfig.value) {
                this.$toastr.error(this.getLang('api_base_required'))
                return
            }
            
            if (!apiKeyConfig || !apiKeyConfig.value) {
                this.$toastr.error(this.getLang('api_key_required'))
                return
            }
            
            this.getModelsIng = true
            this.models = []
            
            // 调用获取模型列表的API
            this.gradioAPI.getOpenAIModels(apiBaseConfig.value, apiKeyConfig.value).then(res => {
                if (res.success) {
                    this.models = res.models || []
                    this.$toastr.success(this.getLang('get_models_success'))
                } else {
                    this.$toastr.error(res.message || this.getLang('get_models_failed'))
                }
                this.getModelsIng = false
            }).catch(err => {
                this.$toastr.error(err.message || this.getLang('get_models_failed'))
                this.getModelsIng = false
            })
        },
        onModelSelect(modelId) {
            // 找到模型配置项并更新其值
            const modelConfig = this.configs.find(c => c.key === 'model')
            if (modelConfig) {
                modelConfig.value = modelId
                // 如果是 select_or_input 类型，同时更新 selectValue
                if (modelConfig.type === 'select_or_input') {
                    modelConfig.selectValue = modelId
                }
            }
        },
        onUnfoldClick(panelName) {
            this.hidePanels[panelName] = !this.hidePanels[panelName]
        },
        onSaveConfigClick() {
            if (this.saveConfigIng) return
            this.saveConfigIng = true
            
            // 保存当前API的配置
            if (!this.apiConfigs[this.selectedApi]) {
                this.apiConfigs[this.selectedApi] = {}
            }
            
            this.configs.forEach(item => {
                this.apiConfigs[this.selectedApi][item.key] = item.value
            })
            
            this.gradioAPI.setData('chatgpt_key', this.apiConfigs).then(res => {
                this.$toastr.success(this.getLang('success'))
                this.saveConfigIng = false
            }).catch(err => {
                this.$toastr.error(err.message || err)
                this.saveConfigIng = false
            })
        },
        onPresetChange(e) {
            this.chatPreset = e.target.value
            this._saveChatPreset()
        },
        onRestoreClick() {
            this.chatPreset = this.getLang('chatgpt_prompts_preset')
            this._saveChatPreset()
        },
        _saveChatPreset() {
            this.gradioAPI.setData('chatgpt_prompts_preset', this.chatPreset)
        },
        onGenClick() {
            if (this.genIng) return
            if (!this.imageDesc) return this.$refs.imageDesc.focus()
            this.imageDesc = this.imageDesc.trim()
            if (!this.imageDesc) return this.$refs.imageDesc.focus()
            this.genIng = true
            let messages = [
                {'role': 'user', 'content': this.chatPreset},
                {'role': 'user', 'content': this.imageDesc},
            ]
            let configs = {}
            this.configs.forEach(item => {
                configs[item.key] = item.value
            })
            this.gradioAPI.genOpenAI(messages, configs).then(res => {
                if (res.success) {
                    this.promptResult = res.result
                } else {
                    this.$toastr.error(res.message || 'error')
                }
                this.genIng = false
            }).catch(err => {
                this.$toastr.error(err.message || err)
                this.genIng = false
            })
        },
        onUseClick() {
            this.$emit('use', this.promptResult)
            this.close()
        },
    },
}
</script>

<style scoped>
.select-or-input-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.select-or-input-container select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: white;
}

.select-or-input-container input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.models-container {
    max-height: 200px;
    overflow-y: auto;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #f9f9f9;
}

.model-item {
    padding: 8px 12px;
    border-bottom: 1px solid #eee;
    cursor: pointer;
    transition: background-color 0.2s;
}

.model-item:last-child {
    border-bottom: none;
}

.model-item:hover {
    background-color: #e9e9e9;
}

.model-name {
    font-weight: bold;
    font-size: 14px;
}

.model-owned-by {
    font-size: 12px;
    color: #666;
    margin-top: 2px;
}
</style>