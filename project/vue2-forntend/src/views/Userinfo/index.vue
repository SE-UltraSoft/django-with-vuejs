<template>
  <div class="app-container">
    <v-app>
      <v-row class="fill-height">
        <v-tabs vertical>
          <v-tab>
            <v-icon left>mdi-account</v-icon>个人信息
          </v-tab>
          <v-tab>
            <v-icon left>mdi-lock</v-icon>基础设置
          </v-tab>
          <!--基础设置-->
          <v-tab-item>
            <v-form ref="form" v-model="form" class="pa-4 pt-6">
              <v-textarea
                v-model="studentname"
                auto-grow
                filled
                color="blue"
                label="name"
                rows="1"
              ></v-textarea>
              <v-textarea
                v-model="studentID"
                auto-grow
                filled
                color="blue"
                label="studentID"
                rows="1"
              ></v-textarea>
              <v-text-field
                v-model="password"
                :rules="[rules.password, rules.length(6)]"
                filled
                color="blue"
                counter="6"
                label="Password"
                style="min-height: 96px"
                type="password"
              ></v-text-field>
              <v-text-field
                v-model="phone"
                filled
                color="blue"
                label="Phone number"
              ></v-text-field>
              <v-text-field
                v-model="email"
                :rules="[rules.email]"
                filled
                color="blue"
                label="Email address"
                type="email"
              ></v-text-field>
              <v-textarea
                v-model="profile"
                auto-grow
                filled
                color="blue"
                label="profile"
                rows="1"
              ></v-textarea>
            </v-form>
            <v-divider></v-divider>
            <v-card-actions>
              <v-btn text @click="$refs.form.reset()">Clear</v-btn>
              <v-spacer></v-spacer>
              <v-btn
                :disabled="!form"
                class="white--text"
                color="blue accent-4"
                depressed
                @click="OnUserInfoSubmit"
              >Submit</v-btn>
            </v-card-actions>
          </v-tab-item>

          <v-tab-item>
            <!--v-card
              class="mx-auto"
              max-width="68%"
            -->
              <v-list shaped>
                <v-subheader>Email通知</v-subheader>
                <v-list-item-group
                  v-model="model"
                  multiple
                >
                  <template v-for="(item, i) in items">
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
                        <v-list-item-content>
                          <v-list-item-title v-text="item"></v-list-item-title>
                        </v-list-item-content>

                        <v-list-item-action>
                          <v-checkbox
                            :input-value="active"
                            :true-value="item"
                            color="blue accent-4"
                            @click="toggle"
                          ></v-checkbox>
                        </v-list-item-action>
                      </template>
                    </v-list-item>
                  </template>
                </v-list-item-group>

                <v-divider
                  class="mx-4"
                  vertical
                ></v-divider>

                <v-subheader>默认提醒时间</v-subheader>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title v-text="`距离截止时间还剩`"></v-list-item-title>
                    <v-row>
                      <v-col cols="auto" >
                        <v-textarea
                          class="mx-2"
                          label="天"
                          rows="1"
                        ></v-textarea>
                      </v-col>
                      <v-col cols="auto" >
                        <v-textarea
                          class="mx-2"
                          label="小时"
                          rows="1"
                        ></v-textarea>
                      </v-col>
                      <v-col cols="auto" >
                        <v-textarea
                          class="mx-2"
                          label="分钟"
                          rows="1"
                        ></v-textarea>
                      </v-col>
                    </v-row>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title v-text="`根据课程个性化设置 ${isCustomization.toString()}`"></v-list-item-title>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-switch v-model="isCustomization"></v-switch>
                  </v-list-item-action>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
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

              </v-list>
            <!--/v-card-->
          </v-tab-item>

        </v-tabs>
      </v-row>
    </v-app>
  </div>
</template>

<script>

import { getUserInfo } from '@/api/user';

export default {
  data: () => ({

    form: false,
    
    studentname: '',
    studentID: '',
    phone: '',
    email: '',
    password: '',
    profile: '',


    rules: {
      email: v => (v || '').match(/@/) || 'Please enter a valid email',
      length: len => v => (v || '').length >= len || `Invalid character length, required ${len}`,
      password: v => (v || '').match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$/) ||
        'Password must contain an upper case letter, a numeric character, and a special character',
      required: v => !!v || 'This field is required',
    },

    items: [
      'DDL提醒',
      '团体日程提醒',
      //'',
      '共享资源更新',
    ],
    model: ['DDL提醒'],

    isCustomization: false,

    ddls: [],
  }),

  created () {
    this.initialize()
  },

  methods:{

    OnUserInfoSubmit() {//传输数据到后台
      this.$message('submit!')
    },

    initialize () {
      
      getUserInfo(this.$store.getters.uid).then(res => {
        console.log(res)
        if (res.data.success) {
          var user_info = res.data.user
          this.studentname = user_info.name
          this.studentID = user_info.student_id
          // this.phone = '18888888888',
          this.email = user_info.email
          // password: 'Hey!ddlkiller123',
          // profile: 'The journey is the reword.',
        }
        else {
          alert(res.data.message)
        }
      })

      this.ddls = [
        {
          name: '计算机科学方法论',
          starts: 159,
          ends: 6.0,
          remains: 24,
          contacts: 4.0,
          glutenfree: false,
          remaintime: '1天12小时20分',
        },
        {
          name: '软件工程（罗杰、任建）',
          starts: 237,
          ends: 9.0,
          remains: 37,
          contacts: 4.3,
          glutenfree: false,
          remaintime: '0天0小时1分',
        },
      ]
    },
  }
}
</script>
