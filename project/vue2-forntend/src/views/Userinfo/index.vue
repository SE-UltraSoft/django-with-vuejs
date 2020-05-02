<template>
<div class="app-container">
  <v-app>
    <v-row class="fill-height">
      <v-tabs vertical>
        <v-tab>
          <v-icon left>mdi-account</v-icon>个人信息
        </v-tab>
        <v-tab>
          <v-icon left>mdi-settings</v-icon>基础设置
        </v-tab>
        <v-tab-item>
          <v-form ref="userForm" class="pa-4 pt-6">
            <v-text-field
              v-model="userForm.name"
              label="用户名"
              outlined
              shaped
              :rules="[rules.name]"
              :readonly="!isChangeName"
              :append-icon="!isChangeName ? 'mdi-border-color' : 'mdi-check'"
              @click:append="isChangeName = !isChangeName"
            ></v-text-field>
            <v-text-field
              v-model="userForm.uid"
              label="学号"
              outlined
              shaped
              readonly
            ></v-text-field>
            <v-text-field
              v-model="userForm.email"
              label="邮箱"
              outlined
              shaped
              :rules="[rules.email]"
              :readonly="!isChangeEmail"
              :append-icon="!isChangeEmail ? 'mdi-border-color' : 'mdi-check'"
              @click:append="isChangeEmail = !isChangeEmail"
            ></v-text-field>
            <v-text-field
              v-model="userForm.passward"
              :label="!isChangePassword ? '修改密码' : '修改密码为'"
              outlined
              shaped
              type="password"
              :readonly="!isChangePassword"
              :append-icon="!isChangePassword ? 'mdi-border-color' : 'mdi-check'"
              @click:append="isChangePassword = !isChangePassword"
            ></v-text-field>
          </v-form>

          <v-divider></v-divider>

          <v-card-actions>
            <v-btn text @click="OnUserInfoClear">Clear</v-btn>
            <v-spacer></v-spacer>
            <v-btn
              class="white--text"
              color="blue accent-4"
              depressed
              :disabled="isChangeEmail||isChangeName||isChangePassword"
              @click="OnUserInfoSubmit"
            >Submit</v-btn>
          </v-card-actions>
        </v-tab-item>

        <v-tab-item>
          <v-list shaped>
            <v-subheader>Email通知</v-subheader>
            <v-list-item-group
              v-model="settings"
              multiple
            >
              <template v-for="(item, i) in emailSets">
                <v-divider
                  v-if="!item"
                  :key="`divider-${i}`"
                ></v-divider>

                <v-list-item
                  v-else
                  :key="`item-${i}`"
                  :value="item"
                  active-class="blue--text text--accent-4"
                >
                  <template v-slot:default="{ active, toggle }">
                    <v-list-item-action>
                      <v-checkbox
                        :input-value="active"
                        :true-value="item"
                        color="blue accent-4"
                        @click="toggle"
                      ></v-checkbox>
                    </v-list-item-action>
                    <v-list-item-content>
                      <v-list-item-title v-text="item"></v-list-item-title>
                    </v-list-item-content>
                  </template>
                </v-list-item>
              </template>
            </v-list-item-group>
          </v-list>
        </v-tab-item>


      </v-tabs>
    </v-row>
  </v-app>
</div>
</template>

<script>
  export default {
    data: () => ({
      isChangeName : false,
      isChangeEmail: false,
      isChangePassword: false,

      rules: {
        name: v => (v || '').length >= 1 || `Please enter a valid name`,
        email: v => (v || '').match(/@/) || 'Please enter a valid email',
        length: len => v => (v || '').length >= len || `Invalid character length, required ${len}`,
      },

      userForm: {
        uid: '17066666',
        name: '小小软',
        email: 'soft@little.com',
        passward: '',
      },

      emailSets: [
        'DDL提醒',
        '团体日程提醒',
        //'',
        '共享资源更新',
      ],
      settings: ['团体日程提醒', 'DDL提醒'],

    }),

    created () {
      this.initialize()
    },

    methods:{
      initialize () {
        getUserInfo(this.$store.getters.uid).then(res => {
          console.log(res)
        })
      },

      OnUserInfoSubmit() {//传输数据到后台
        var valid = this.$refs.userForm.validate()
        if(valid) {
          //向后端传数据
          register(this.$refs.userForm).then(res => {
            this.$message('submit!');
          }).catch(error => {
            alert(error)
          })
        }
        else {
          this.$message('error submit!')
        }
      },
      OnUserInfoClear() {
        //重置表单
        // this.$refs.userForm.reset()
        this.userForm.name = ''
        this.userForm.email = ''
        this.userForm.passward = ''
      },
    },
  }
</script>
