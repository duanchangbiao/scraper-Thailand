<script setup lang="ts">
import {computed, ref, watch} from 'vue';
import {useAntdForm, useFormRules} from '@/hooks/common/form';
import {fetchGetAllRoles, fetchSaveUser} from '@/service/api';
import {$t} from '@/locales';
import {enableStatusOptions, userGenderOptions} from '@/constants/business';
import SimpleScrollbar from '~/packages/materials/src/libs/simple-scrollbar/index.vue';

defineOptions({
  name: 'UserOperateDrawer'
});

interface Props {
  /** the type of operation */
  operateType: AntDesign.TableOperateType;
  /** the edit row data */
  rowData?: Api.SystemManage.User | null;
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
  const titles: Record<AntDesign.TableOperateType, string> = {
    add: $t('page.manage.user.addUser'),
    edit: $t('page.manage.user.editUser')
  };
  return titles[props.operateType];
});

type Model = Pick<
  Api.SystemManage.User,
  'username' | 'sex' | 'nickname' | 'phone' | 'email' | 'status' | 'password' | 'isActive'
>;

const model = ref(createDefaultModel());

function createDefaultModel(): {
  password: string;
  phone: string;
  sex: string;
  nickname: string;
  isActive: number;
  email: string;
  username: string;
  status: string;
  userRole: {
    roleId: string,
    roleName: string
  }
} {
  return {
    username: '',
    password: '',
    sex: '1',
    nickname: '',
    phone: '',
    email: '',
    isActive: 1,
    status: '1',
    userRole: {
      roleId: '',
      roleName: ''
    }
  };
}

type RuleKey = Extract<keyof Model, 'username' | 'status' | 'password' | 'nickname' | 'isActive' | 'phone' | 'email' | 'roleId'>;

const rules: Record<RuleKey, App.Global.FormRule> = {
  username: defaultRequiredRule,
  status: defaultRequiredRule,
  password: defaultRequiredRule,
  nickname: defaultRequiredRule,
  isActive: defaultRequiredRule,
  phone: defaultRequiredRule,
  email: defaultRequiredRule,
};

/** the enabled role options */
const roleOptions = ref<CommonType.Option<string>[]>([]);

async function getRoleOptions() {
  const {error, data} = await fetchGetAllRoles();

  if (!error) {
    const options = data.map(item => ({
      label: item.roleName,
      value: item.roleId
    }));

    // the mock data does not have the roleCode, so fill it
    // if the real request, remove the following code
    const userRoleOptions = [
      {
        label: model.value.userRole.roleName,
        value: model.value.userRole.roleId
    }]

    // end

    roleOptions.value = [...userRoleOptions, ...options];
  }
}

function handleInitModel() {
  model.value = createDefaultModel();

  if (props.operateType === 'edit' && props.rowData) {
    Object.assign(model.value, props.rowData);
  }
}

function closeDrawer() {
  visible.value = false;
}

async function handleSubmit() {
  await validate();
  // request
  const {error, data} = await fetchSaveUser(model.value)
  window.$message?.success($t('common.updateSuccess'));
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
</script>

<template>
  <AModal v-model:open="visible" :title="title" width="600px">
    <div class="h-480px">
      <SimpleScrollbar>
        <AForm
          ref="formRef"
          layout="horizontal"
          :model="model"
          :rules="rules"
          :label-col="{ span: 5 }"
          :wrapper-col="{ span: 15 }"
        >
          <AFormItem :label="$t('page.manage.user.username')" name="username">
            <AInput v-model:value="model.username" :placeholder="$t('page.manage.user.form.username')"/>
          </AFormItem>
          <AFormItem :label="$t('page.manage.user.password')" name="password">
            <AInputPassword v-model:value="model.password" :placeholder="$t('page.manage.user.form.password')"/>
          </AFormItem>
          <AFormItem :label="$t('page.manage.user.sex')" name="sex">
            <ARadioGroup v-model:value="model.sex">
              <ARadio v-for="item in userGenderOptions" :key="item.value" :value="item.value">
                {{ $t(item.label) }}
              </ARadio>
            </ARadioGroup>
          </AFormItem>
          <AFormItem :label="$t('page.manage.user.nickname')" name="nickname">
            <AInput v-model:value="model.nickname" :placeholder="$t('page.manage.user.form.nickname')"/>
          </AFormItem>
          <AFormItem :label="$t('page.manage.user.phone')" name="phone">
            <AInput v-model:value="model.phone" :placeholder="$t('page.manage.user.form.phone')"/>
          </AFormItem>
          <AFormItem :label="$t('page.manage.user.email')" name="email">
            <AInput v-model:value="model.email" :placeholder="$t('page.manage.user.form.email')"/>
          </AFormItem>
          <AFormItem :label="$t('page.manage.user.status')" name="status">
            <ARadioGroup v-model:value="model.status">
              <ARadio v-for="item in enableStatusOptions" :key="item.value" :value="item.value">
                {{ $t(item.label) }}
              </ARadio>
            </ARadioGroup>
          </AFormItem>
          <AFormItem :label="$t('page.manage.user.userRole.roleName')" name="userRole">
            <ASelect
              v-model:value="model.userRole.roleName"
              :options="roleOptions"
              :placeholder="$t('page.manage.user.form.userRole')"
            />
          </AFormItem>
        </AForm>
      </SimpleScrollbar>
    </div>
    <template #footer>
      <ASpace :size="16">
        <AButton @click="closeDrawer">{{ $t('common.cancel') }}</AButton>
        <AButton type="primary" @click="handleSubmit">{{ $t('common.confirm') }}</AButton>
      </ASpace>
    </template>
  </AModal>
</template>

<style scoped></style>
