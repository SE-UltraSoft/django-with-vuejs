<template>
  <div class="app-container">
    <v-app>
      <v-row class="fill-height">
        <v-rol>
          <template>
              <v-tabs vertical>
                <v-tab>
                  <v-icon left>mdi-account</v-icon>
                  个人信息
                </v-tab>
                <v-tab>
                  <v-icon left>mdi-lock</v-icon>
                  基础设置
                </v-tab>

                <v-tab-item>
                  <!--v-card flat>
                    <v-list two-line>
                      <v-list-item @click="">

                        <v-list-item-icon>
                          <v-icon color="indigo">mdi-message-text</v-icon>
                        </v-list-item-icon>

                        <v-list-item-content>
                          <v-list-item-title>17060001</v-list-item-title>
                          <v-list-item-subtitle>Student Id</v-list-item-subtitle>
                        </v-list-item-content>

                      </v-list-item>

                      <v-list-item @click="">
                        <v-list-item-icon>
                          <v-icon color="indigo">mdi-phone</v-icon>
                        </v-list-item-icon>

                        <v-list-item-content>
                          <v-list-item-title>空空</v-list-item-title>
                          <v-list-item-subtitle>Name</v-list-item-subtitle>
                        </v-list-item-content>

                      </v-list-item>

                      <v-divider inset></v-divider>

                      <v-list-item @click="">
                        <v-list-item-icon>
                          <v-icon color="indigo">mdi-email</v-icon>
                        </v-list-item-icon>

                        <v-list-item-content>
                          <v-list-item-title>aliconnors@example.com</v-list-item-title>
                          <v-list-item-subtitle>Email</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>

                      <v-divider inset></v-divider>

                      <v-list-item @click="">
                        <v-list-item-icon>
                          <v-icon color="indigo">mdi-map-marker</v-icon>
                        </v-list-item-icon>


                        <v-list-item-content>
                          <v-list-item-title>普通学生</v-list-item-title>
                          <v-list-item-subtitle>User Level</v-list-item-subtitle>
                        </v-list-item-content>

                      </v-list-item>
                    </v-list>
                  </v-card-->
                  <v-card flat>
                    <el-form ref="form" :model="form" label-width="400px">
                      <el-form-item label="姓名">
                        <el-input v-model="form.name" placeholder="请输入您的姓名"/>
                      </el-form-item>
                      <el-form-item label="学号">
                        <el-input v-model="form.studentID" placeholder="请输入您的学号"/>
                      </el-form-item>
                      <el-form-item label="邮箱">
                        <el-input v-model="form.email" placeholder="请输入您的邮箱"/>
                      </el-form-item>
                      <el-form-item label="密码">
                        <el-input v-model="form.password" placeholder="请输入密码" show-password></el-input>
                      </el-form-item>
                      <el-form-item label="用户类型">
                        <el-select v-model="form.region" placeholder="">
                          <el-option label="学生" value="student" />
                          <el-option label="助教" value="assistant" />
                          <el-option label="老师" value="teather" />
                        </el-select>
                      </el-form-item>
                      <el-form-item label="个人简介">
                        <el-input v-model="form.desc" type="textarea" autosize/>
                      </el-form-item>
                      <el-form-item>
                        <el-button type="primary" @click="onUserSubmit">保存</el-button>
                      </el-form-item>
                    </el-form>
                  </v-card>
                </v-tab-item>

                <v-tab-item>
                  <v-card flat>
                    <v-list
                      flat
                      subheader
                      three-line
                    >
                      <v-subheader>Email通知</v-subheader>

                      <v-list-item-group
                        v-model="settings"
                        multiple
                      >
                        <v-list-item>
                            <v-list-item-action>
                              <v-checkbox v-model="active"></v-checkbox>
                            </v-list-item-action>

                            <v-list-item-content>
                              <v-list-item-title>DDL提醒</v-list-item-title>
                              <v-list-item-subtitle>Notify me about updates to apps or games that I downloaded</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>

                        <v-list-item>
                            <v-list-item-action>
                              <v-checkbox v-model="active"></v-checkbox>
                            </v-list-item-action>

                            <v-list-item-content>
                              <v-list-item-title>团体日程提醒</v-list-item-title>
                              <v-list-item-subtitle>Auto-update apps at any time. Data charges may apply</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>

                        <v-list-item>
                            <v-list-item-action>
                              <v-checkbox v-model="active"></v-checkbox>
                            </v-list-item-action>

                            <v-list-item-content>
                              <v-list-item-title>共享资源更新</v-list-item-title>
                              <v-list-item-subtitle>Automatically add home screen widgets when downloads complete</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>
                      </v-list-item-group>

                    </v-list>

                    <v-list
                      flat
                      subheader
                      three-line
                    >
                      <v-subheader>默认提醒时间</v-subheader>
                        <v-list-item-group
                          v-model="settings"
                          multiple
                        >
                          <v-list-item>
                              <v-list-item-content>
                                <!--v-list-item-title>账户默认提醒时间</v-list-item-title-->
                                <el-form :inline="true" :model="downloadInline" class="demo-form-inline">
                                  <el-form-item label="距离截止时间还剩"></el-form-item>
                                  <el-form-item label="">
                                    <el-input v-model="defaultDRemainer" placeholder="天"></el-input>
                                  </el-form-item>
                                  <el-form-item label="天"></el-form-item>
                                  <el-form-item label="">
                                    <el-input v-model="defaultHRemainer" placeholder="时"></el-input>
                                  </el-form-item>
                                  <el-form-item label="时"></el-form-item>
                                  <el-form-item label="">
                                    <el-input v-model="defaultMRemainer" placeholder="分"></el-input>
                                  </el-form-item label="">
                                    <el-form-item label="分"></el-form-item>
                                  <el-form-item>
                                    <el-button type="primary" @click="onRemainerSubmit">保存</el-button>
                                  </el-form-item>
                                </el-form>
                              </v-list-item-content>
                          </v-list-item>

                          <v-list-item>
                            <v-list-item-content>
                              <v-list-item-title>根据课程个性化设置</v-list-item-title>
                              <v-switch v-model="isCustomization"  :label="` ${isCustomization.toString()}`"></v-switch>
                              <template>
                                <v-simple-table v-show="isCustomization">
                                  <template v-slot:default>
                                    <thead>
                                      <tr>
                                        <th class="text-left">课程名称</th>
                                        <th class="text-left">截止时间</th>
                                      </tr>
                                    </thead>
                                    <tbody>
                                      <tr v-for="item in ddls" :key="item.name">
                                        <td>{{ item.name }}</td>
                                        <td>{{ item.remaintime }}</td>
                                      </tr>
                                    </tbody>
                                  </template>
                                </v-simple-table>
                              </template>
                            </v-list-item-content>
                          </v-list-item>

                        </v-list-item-group>
                    </v-list>

                  </v-card>
                </v-tab-item>

              </v-tabs>
          </template>

        </v-rol>
      </v-row>
    </v-app>
  </div>

</template>

<script>
  export default {
    data () {
      return {

        defaultDRemainer: '',
        defaultHRemainer: '',
        defaultMRemainer: '',

        form: {
          name: '',
          studentID: '',
          email: '',
          password: '',
          region: '',
          desc: '',
        },

        isCustomization: false,

        ddls: [
          {
            name: 'Frozen Yogurt',
            remaintime: '2h15m',
          },
          {
            name: 'Ice cream sandwich',
            remaintime: '3h15m',
          },
          {
            name: 'Eclair',
            remaintime: '5h15m',
          },
        ],
        

      }
    },

    methods: {
      onUserSubmit() {

        this.$message('submit!');
        console.log(this.form)
      },

      onRemainerSubmit() {
        this.$message('submit!')
      },
    },

  }

</script>

<style scoped>
.line{
  text-align: center;
}
</style>
