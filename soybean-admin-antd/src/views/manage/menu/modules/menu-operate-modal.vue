<script setup lang="tsx">
import {computed, nextTick, ref, watch} from 'vue';
import {SimpleScrollbar} from '@sa/materials';
import {useAntdForm, useFormRules} from '@/hooks/common/form';
import {$t} from '@/locales';
import {enableStatusOptions, menuIconTypeOptions, menuTypeOptions} from '@/constants/business';
import SvgIcon from '@/components/custom/svg-icon.vue';
import {getLocalIcons} from '@/utils/icon';
import {fetchGetAllRoles, insertSaveMenuInfo, insertSaveRoleInfo, updateMenuInfo, updateRoleInfo} from '@/service/api';
import {
  getLayoutAndPage,
  getPathParamFromRoutePath,
  getRoutePathByRouteName,
  getRoutePathWithParam,
  transformLayoutAndPageToComponent
} from './shared';

defineOptions({
  name: 'MenuOperateModal'
});

export type OperateType = AntDesign.TableOperateType | 'addChild';

interface Props {
  /** the type of operation */
  operateType: OperateType;
  /** the edit menu data or the parent menu data when adding a child menu */
  rowData?: Api.SystemManage.Menu | null;
  /** all pages */
  allPages: string[];
}

const props = defineProps<Props>();

interface Emits {
  (e: 'submitted'): void;
}

const emit = defineEmits<Emits>();

const visible = defineModel<boolean>('visible', {
  default: false
});

const {formRef, validate, resetFields} = useAntdForm();
const {defaultRequiredRule} = useFormRules();

const title = computed(() => {
  const titles: Record<OperateType, string> = {
    add: $t('page.manage.menu.addMenu'),
    addChild: $t('page.manage.menu.addChildMenu'),
    edit: $t('page.manage.menu.editMenu')
  };
  return titles[props.operateType];
});

type Model = Pick<
  Api.SystemManage.Menu,
  | 'menuType'
  | 'menuName'
  | 'routeName'
  | 'routePath'
  | 'component'
  | 'order'
  | 'i18nKey'
  | 'icon'
  | 'iconType'
  | 'status'
  | 'parentId'
  | 'keepAlive'
  | 'constant'
  | 'href'
  | 'hideInMenu'
  | 'activeMenu'
  | 'multiTab'
  | 'fixedIndexInTab'
> & {
  query: NonNullable<Api.SystemManage.Menu['query']>;
  buttons: NonNullable<Api.SystemManage.Menu['buttons']>;
  layout: string;
  page: string;
  pathParam: string;
};

const model = ref(createDefaultModel());

function createDefaultModel(): Model {
  return {
    menuType: '1',
    menuName: '',
    routeName: '',
    routePath: '',
    pathParam: '',
    component: '',
    layout: '',
    page: '',
    i18nKey: null,
    icon: '',
    iconType: '1',
    parentId: 0,
    status: '1',
    keepAlive: false,
    constant: false,
    order: 0,
    href: null,
    hideInMenu: false,
    activeMenu: null,
    multiTab: false,
    fixedIndexInTab: null,
    query: [],
    buttons: []
  };
}

type RuleKey = Extract<keyof Model, 'menuName' | 'status' | 'routeName' | 'routePath'>;

const rules: Record<RuleKey, App.Global.FormRule> = {
  menuName: defaultRequiredRule,
  status: defaultRequiredRule,
  routeName: defaultRequiredRule,
  routePath: defaultRequiredRule
};

const disabledMenuType = computed(() => props.operateType === 'edit');

const localIcons = getLocalIcons();
const localIconOptions = localIcons.map(item => ({
  label: () => (
    <div class="flex-y-center gap-16px">
      <SvgIcon localIcon={item} class="text-icon"/>
      <span>{item}</span>
    </div>
  ),
  value: item
}));

const showLayout = computed(() => model.value.parentId === 0);

const showPage = computed(() => model.value.menuType === '2');

const pageOptions = computed(() => {
  const allPages = [...props.allPages];

  if (model.value.routeName && !allPages.includes(model.value.routeName)) {
    allPages.unshift(model.value.routeName);
  }

  const opts: CommonType.Option[] = allPages.map(page => ({
    label: page,
    value: page
  }));

  return opts;
});

const layoutOptions: CommonType.Option[] = [
  {
    label: 'base',
    value: 'base'
  },
  {
    label: 'blank',
    value: 'blank'
  }
];

/** the enabled role options */
const roleOptions = ref<CommonType.Option<string>[]>([]);

async function getRoleOptions() {
  const {error, data} = await fetchGetAllRoles();
  if (!error) {
    const options = data.map(item => ({
      label: item.roleName,
      value: item.roleCode
    }));

    roleOptions.value = [...options];
  }
}

/** - add a query input */
// function addQuery(index: number) {
//   model.value.query.splice(index + 1, 0, {
//     key: '',
//     value: ''
//   });
// }

/** - remove a query input */
// function removeQuery(index: number) {
//   model.value.query.splice(index, 1);
// }

/** - add a button input */
// function addButton(index: number) {
//   model.value.buttons.splice(index + 1, 0, {
//     code: '',
//     desc: ''
//   });
// }

/** - remove a button input */
// function removeButton(index: number) {
//   model.value.buttons.splice(index, 1);
// }

async function handleInitModel() {
  model.value = createDefaultModel();
  if (!props.rowData) return;
  await nextTick();

  if (props.operateType === 'addChild') {
    const {id} = props.rowData;

    Object.assign(model.value, {parentId: id});
  }

  if (props.operateType === 'edit') {
    const {component, ...rest} = props.rowData;

    const {layout, page} = getLayoutAndPage(component);
    const {path, param} = getPathParamFromRoutePath(rest.routePath);

    Object.assign(model.value, rest, {layout, page, routePath: path, pathParam: param});
  }

  if (!model.value.query) {
    model.value.query = [];
  }
  if (!model.value.buttons) {
    model.value.buttons = [];
  }
}

function closeDrawer() {
  visible.value = false;
}

function handleUpdateRoutePathByRouteName() {
  if (model.value.routeName) {
    model.value.routePath = getRoutePathByRouteName(model.value.routeName);
  } else {
    model.value.routePath = '';
  }
}

function handleUpdateI18nKeyByRouteName() {
  if (model.value.routeName) {
    model.value.i18nKey = `route.${model.value.routeName}` as App.I18n.I18nKey;
  } else {
    model.value.i18nKey = null;
  }
}

function getSubmitParams() {
  const {layout, page, pathParam, ...params} = model.value;

  const component = transformLayoutAndPageToComponent(layout, page);
  const routePath = getRoutePathWithParam(model.value.routePath, pathParam);

  params.component = component;
  params.routePath = routePath;

  return params;
}

async function handleSubmit() {
  await validate()
  const params = getSubmitParams();
  if (props.operateType === 'add' || props.operateType === 'addChild') {
    const {error, response} = await insertSaveMenuInfo(params)
    if (!error) {
      if (response.data.success) {
        window.$message?.success($t('common.addSuccess'));
      } else {
        window.$message?.error(response.data.msg);
      }
    }
  } else {
    const {error, response} = await updateMenuInfo(params)
    if (!error) {
      if (response.data.success) {
        window.$message?.success($t('common.updateSuccess'));
      } else {
        window.$message?.error(response.data.msg);
      }
    }

  }
  closeDrawer();
  emit('submitted');
}

watch(visible, () => {
  if (visible.value) {
    handleInitModel();
    resetFields();
    getRoleOptions();
  }
});

watch(
  () => model.value.routeName,
  () => {
    handleUpdateRoutePathByRouteName();
    handleUpdateI18nKeyByRouteName();
  }
);
</script>

<template>
  <AModal v-model:open="visible" :title="title" width="800px">
    <div class="h-350px">
      <SimpleScrollbar>
        <AForm ref="formRef" :model="model" :rules="rules" :label-col="{ lg: 8, xs: 4 }" label-wrap class="pr-20px">
          <ARow>
            <ACol :lg="12" :xs="24">
              <AFormItem :label="$t('page.manage.menu.menuType')" name="menuType">
                <ARadioGroup v-model:value="model.menuType" :disabled="disabledMenuType">
                  <ARadio v-for="item in menuTypeOptions" :key="item.value" :value="item.value">
                    {{ $t(item.label) }}
                  </ARadio>
                </ARadioGroup>
              </AFormItem>
            </ACol>
            <ACol :lg="12" :xs="24">
              <AFormItem :label="$t('page.manage.menu.menuName')" name="menuName">
                <AInput v-model:value="model.menuName" :placeholder="$t('page.manage.menu.form.menuName')"/>
              </AFormItem>
            </ACol>
            <ACol :lg="12" :xs="24">
              <AFormItem :label="$t('page.manage.menu.routeName')" name="routeName">
                <AInput v-model:value="model.routeName" :placeholder="$t('page.manage.menu.form.routeName')"/>
              </AFormItem>
            </ACol>
            <ACol :lg="12" :xs="24">
              <AFormItem :label="$t('page.manage.menu.routePath')" name="routePath">
                <AInput v-model:value="model.routePath" disabled :placeholder="$t('page.manage.menu.form.routePath')"/>
              </AFormItem>
            </ACol>
            <ACol :lg="12" :xs="24">
              <AFormItem :label="$t('page.manage.menu.pathParam')" name="pathParam">
                <AInput v-model:value="model.pathParam" :placeholder="$t('page.manage.menu.form.pathParam')"/>
              </AFormItem>
            </ACol>
            <!--            <ACol :lg="12" :xs="24">-->
            <!--              <AFormItem v-if="showLayout" :label="$t('page.manage.menu.layout')" name="layout">-->
            <!--                <ASelect-->
            <!--                  v-model:value="model.layout"-->
            <!--                  :options="layoutOptions"-->
            <!--                  :placeholder="$t('page.manage.menu.form.layout')"-->
            <!--                />-->
            <!--              </AFormItem>-->
            <!--            </ACol>-->
            <ACol v-if="showPage" :lg="12" :xs="24">
              <AFormItem :label="$t('page.manage.menu.page')" name="page">
                <ASelect
                  v-model:value="model.page"
                  :options="pageOptions"
                  :placeholder="$t('page.manage.menu.form.page')"
                />
              </AFormItem>
            </ACol>
            <!--            <ACol :lg="12" :xs="24">-->
            <!--              <AFormItem :label="$t('page.manage.menu.i18nKey')" name="i18nKey">-->
            <!--                <AInput v-model:value="model.i18nKey as string" :placeholder="$t('page.manage.menu.form.i18nKey')"/>-->
            <!--              </AFormItem>-->
            <!--            </ACol>-->
            <ACol :lg="12" :xs="24">
              <AFormItem :label="$t('page.manage.menu.order')" name="order">
                <AInputNumber
                  v-model:value="model.order as number"
                  class="w-full"
                  :placeholder="$t('page.manage.menu.form.order')"
                />
              </AFormItem>
            </ACol>
            <ACol :lg="12" :xs="24">
              <AFormItem :label="$t('page.manage.menu.iconTypeTitle')" name="iconType">
                <ARadioGroup v-model:value="model.iconType">
                  <ARadio v-for="item in menuIconTypeOptions" :key="item.value" :value="item.value">
                    {{ $t(item.label) }}
                  </ARadio>
                </ARadioGroup>
              </AFormItem>
            </ACol>

            <ACol :lg="12" :xs="24">
              <AFormItem :label="$t('page.manage.menu.icon')" name="icon">
                <template v-if="model.iconType === '1'">
                  <AInput v-model:value="model.icon" :placeholder="$t('page.manage.menu.form.icon')" class="flex-1">
                    <template #suffix>
                      <SvgIcon v-if="model.icon" :icon="model.icon" class="text-icon"/>
                    </template>
                  </AInput>
                </template>
                <template v-if="model.iconType === '2'">
                  <ASelect
                    v-model:value="model.icon"
                    :placeholder="$t('page.manage.menu.form.localIcon')"
                    :options="localIconOptions"
                  />
                </template>
              </AFormItem>
            </ACol>
            <ACol :lg="12" :xs="24">
              <AFormItem :label="$t('page.manage.menu.menuStatus')" name="menuStatus">
                <ARadioGroup v-model:value="model.menuStatus">
                  <ARadio v-for="item in enableStatusOptions" :key="item.value" :value="item.value">
                    {{ $t(item.label) }}
                  </ARadio>
                </ARadioGroup>
              </AFormItem>
            </ACol>
            <ACol :lg="12" :xs="24">
              <AFormItem :label="$t('page.manage.menu.keepAlive')" name="keepAlive">
                <ARadioGroup v-model:value="model.keepAlive">
                  <ARadio :value="true">{{ $t('common.yesOrNo.yes') }}</ARadio>
                  <ARadio :value="false">{{ $t('common.yesOrNo.no') }}</ARadio>
                </ARadioGroup>
              </AFormItem>
            </ACol>
            <!--            <ACol :lg="12" :xs="24">-->
            <!--              <AFormItem :label="$t('page.manage.menu.constant')" name="constant">-->
            <!--                <ARadioGroup v-model:value="model.constant">-->
            <!--                  <ARadio value>-->
            <!--                    {{ $t('common.yesOrNo.yes') }}-->
            <!--                  </ARadio>-->
            <!--                  <ARadio :value="false">-->
            <!--                    {{ $t('common.yesOrNo.no') }}-->
            <!--                  </ARadio>-->
            <!--                </ARadioGroup>-->
            <!--              </AFormItem>-->
            <!--            </ACol>-->
            <ACol :lg="12" :xs="24">
              <AFormItem :label="$t('page.manage.menu.href')" name="href">
                <AInput v-model:value="model.href as string" :placeholder="$t('page.manage.menu.form.href')"/>
              </AFormItem>
            </ACol>
            <ACol :lg="12" :xs="24">
              <AFormItem :label="$t('page.manage.menu.hideInMenu')" name="hideInMenu">
                <ARadioGroup v-model:value="model.hideInMenu">
                  <ARadio :value="'1'">{{ $t('common.yesOrNo.yes') }}</ARadio>
                  <ARadio :value="'0'">{{ $t('common.yesOrNo.no') }}</ARadio>
                </ARadioGroup>
              </AFormItem>
            </ACol>
            <ACol v-if="model.hideInMenu" :lg="12" :xs="24">
              <AFormItem :label="$t('page.manage.menu.activeMenu')" name="activeMenu">
                <ASelect
                  v-model:value="model.activeMenu as string"
                  :options="pageOptions"
                  clearable
                  :placeholder="$t('page.manage.menu.form.activeMenu')"
                />
              </AFormItem>
            </ACol>
            <!--            <ACol :lg="12" :xs="24">-->
            <!--              <AFormItem :label="$t('page.manage.menu.multiTab')" name="multiTab">-->
            <!--                <ARadioGroup v-model:value="model.multiTab">-->
            <!--                  <ARadio value :label="$t('common.yesOrNo.yes')"/>-->
            <!--                  <ARadio :value="false" :label="$t('common.yesOrNo.no')"/>-->
            <!--                </ARadioGroup>-->
            <!--              </AFormItem>-->
            <!--            </ACol>-->
            <!--            <ACol :lg="12" :xs="24">-->
            <!--              <AFormItem :label="$t('page.manage.menu.fixedIndexInTab')" name="fixedIndexInTab">-->
            <!--                <AInputNumber-->
            <!--                  v-model:value="model.fixedIndexInTab as number"-->
            <!--                  class="w-full"-->
            <!--                  clearable-->
            <!--                  :placeholder="$t('page.manage.menu.form.fixedIndexInTab')"-->
            <!--                />-->
            <!--              </AFormItem>-->
            <!--            </ACol>-->
            <!--            <ACol :span="24">-->
            <!--              <AFormItem :label-col="{ span: 4 }" :label="$t('page.manage.menu.query')" name="query">-->
            <!--                <AButton v-if="model.query.length === 0" type="dashed" block @click="addQuery(-1)">-->
            <!--                  <template #icon>-->
            <!--                    <icon-carbon-add class="align-sub text-icon" />-->
            <!--                  </template>-->
            <!--                  <span class="ml-8px">{{ $t('common.add') }}</span>-->
            <!--                </AButton>-->
            <!--                <template v-else>-->
            <!--                  <div v-for="(item, index) in model.query" :key="index" class="flex gap-3">-->
            <!--                    <ACol :span="9">-->
            <!--                      <AFormItem :name="['query', index, 'key']">-->
            <!--                        <AInput-->
            <!--                          v-model:value="item.key"-->
            <!--                          :placeholder="$t('page.manage.menu.form.queryKey')"-->
            <!--                          class="flex-1"-->
            <!--                        />-->
            <!--                      </AFormItem>-->
            <!--                    </ACol>-->
            <!--                    <ACol :span="9">-->
            <!--                      <AFormItem :name="['query', index, 'value']">-->
            <!--                        <AInput-->
            <!--                          v-model:value="item.value"-->
            <!--                          :placeholder="$t('page.manage.menu.form.queryValue')"-->
            <!--                          class="flex-1"-->
            <!--                        />-->
            <!--                      </AFormItem>-->
            <!--                    </ACol>-->
            <!--                    <ACol :span="5">-->
            <!--                      <ASpace class="ml-12px">-->
            <!--                        <AButton size="middle" @click="addQuery(index)">-->
            <!--                          <template #icon>-->
            <!--                            <icon-ic:round-plus class="align-sub text-icon" />-->
            <!--                          </template>-->
            <!--                        </AButton>-->
            <!--                        <AButton size="middle" @click="removeQuery(index)">-->
            <!--                          <template #icon>-->
            <!--                            <icon-ic-round-remove class="align-sub text-icon" />-->
            <!--                          </template>-->
            <!--                        </AButton>-->
            <!--                      </ASpace>-->
            <!--                    </ACol>-->
            <!--                  </div>-->
            <!--                </template>-->
            <!--              </AFormItem>-->
            <!--            </ACol>-->
            <!--            <ACol :span="24">-->
            <!--              <AFormItem :label-col="{ span: 4 }" :label="$t('page.manage.menu.button')" name="buttons">-->
            <!--                <AButton v-if="model.buttons.length === 0" type="dashed" block @click="addButton(-1)">-->
            <!--                  <template #icon>-->
            <!--                    <icon-carbon-add class="align-sub text-icon" />-->
            <!--                  </template>-->
            <!--                  <span class="ml-8px">{{ $t('common.add') }}</span>-->
            <!--                </AButton>-->
            <!--                <template v-else>-->
            <!--                  <div v-for="(item, index) in model.buttons" :key="index" class="flex gap-3">-->
            <!--                    <ACol :span="9">-->
            <!--                      <AFormItem :name="['buttons', index, 'code']">-->
            <!--                        <AInput-->
            <!--                          v-model:value="item.code"-->
            <!--                          :placeholder="$t('page.manage.menu.form.buttonCode')"-->
            <!--                          class="flex-1"-->
            <!--                        ></AInput>-->
            <!--                      </AFormItem>-->
            <!--                    </ACol>-->
            <!--                    <ACol :span="9">-->
            <!--                      <AFormItem :name="['buttons', index, 'desc']">-->
            <!--                        <AInput-->
            <!--                          v-model:value="item.desc"-->
            <!--                          :placeholder="$t('page.manage.menu.form.buttonDesc')"-->
            <!--                          class="flex-1"-->
            <!--                        ></AInput>-->
            <!--                      </AFormItem>-->
            <!--                    </ACol>-->
            <!--                    <ACol :span="5">-->
            <!--                      <ASpace class="ml-12px">-->
            <!--                        <AButton size="middle" @click="addButton(index)">-->
            <!--                          <template #icon>-->
            <!--                            <icon-ic:round-plus class="align-sub text-icon" />-->
            <!--                          </template>-->
            <!--                        </AButton>-->
            <!--                        <AButton size="middle" @click="removeButton(index)">-->
            <!--                          <template #icon>-->
            <!--                            <icon-ic-round-remove class="align-sub text-icon" />-->
            <!--                          </template>-->
            <!--                        </AButton>-->
            <!--                      </ASpace>-->
            <!--                    </ACol>-->
            <!--                  </div>-->
            <!--                </template>-->
            <!--              </AFormItem>-->
            <!--            </ACol>-->
          </ARow>
        </AForm>
      </SimpleScrollbar>
    </div>
    <template #footer>
      <ASpace justify="end" :size="16">
        <AButton @click="closeDrawer">{{ $t('common.cancel') }}</AButton>
        <AButton type="primary" @click="handleSubmit">{{ $t('common.confirm') }}</AButton>
      </ASpace>
    </template>
  </AModal>
</template>

<style scoped></style>
