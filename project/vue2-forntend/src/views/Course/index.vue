<template>
  <div class="app-container">
    <v-app>
      <v-toolbar flat>
        <v-chip-group
          column
          active-class="primary--text"
        >
          <v-chip v-for="tag in tags" :key="tag.cid" @click="chooseOne(tag)"
            class="ma-2" color="#1565C0" outlined label
          >
            {{ tag.course_name }}
          </v-chip>
        </v-chip-group>

        <template v-slot:extension>
          <v-tabs>
            <v-tab>DDL列表</v-tab>
            <v-tab>共享资源</v-tab>

            <!--DDL列表 开始-->
            <v-tab-item>
              <!--Eventlist></Eventlist-->
              <v-data-table
                :headers="headers"
                :items="ddls"
                class="elevation-1"
                show-expand
                single-expand=true
                :expanded.sync="expanded"
                item-key="tid"
              >
                <!--template v-slot:item.remains="{ item }">
                  <v-chip :color="getColor(item.remains)" dark>{{ item.remains }}</v-chip>
                </template-->

                <template v-slot:item.title="{ item }">
                  <a v-bind:href="item.urls"> {{item.title}}</a>
                </template>

                <template v-slot:item.is_finished="{ item }">
                  <v-simple-checkbox v-model="item.is_finished"></v-simple-checkbox>
                </template>

                <template v-slot:expanded-item="{ headers, item }">
                  <td :colspan="headers.length">{{ item.content }}</td>
                </template>

              </v-data-table>

            </v-tab-item>
            <!--DDL列表 结束-->

            <v-tab-item>
              <v-simple-table class="elevation-1">
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th class="text-left">资源名称</th>
                      <th class="text-left">提取码</th>
                      <!--th class="text-left">分享人</th-->
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in srcs" :key="item.rid">
                      <td><a v-bind:href="item.url"> {{item.title}}</a></td>
                      <td v-if="item.code!=''">{{ item.code }}</td>
                      <td v-else></td>
                      <!--td>{{ item.sharer }}</td-->
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>

              <v-divider></v-divider>

              <v-col>
                <el-form :inline="true" :model="fileSubmit" class="demo-form-inline">
                  <el-form-item label="文件名">
                    <el-input v-model="fileSubmit.ftitle" placeholder="文件名"></el-input>
                  </el-form-item>
                  <el-form-item label="分享链接">
                    <el-input v-model="fileSubmit.furl" placeholder="分享链接"></el-input>
                  </el-form-item>
                  <el-form-item label="提取码">
                    <el-input v-model="fileSubmit.fpss" placeholder="提取码"></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" :disabled="!(fileSubmit.furl&&fileSubmit.ftitle)" @click="onFileSubmit">分享</el-button>
                  </el-form-item>
                </el-form>
              </v-col>

            </v-tab-item>
          </v-tabs>
        </template>

      </v-toolbar>
    </v-app>
  </div>
</template>

<script>
  import { getUserCourses } from '@/api/course';
  import { getCourseByCid } from '@/api/course';
  import { getResourceByCid } from '@/api/course';
  import Eventlist from '../Eventlist/index.vue'
  //DDL列表 开始
  //DDL列表 结束

  export default {
    components: {
      Eventlist,
    },

    data: () => ({
      ////////////////////////////////////DDL列表 开始
      headers: [
        {
          text: '事项名称',
          align: 'start',
          sortable: false,
          value: 'title',
        },
        { text: '发布时间', value: 'create_time' },
        { text: '截止时间', value: 'ddl_time' },
        //{ text: '剩余时间', value: 'remains' },
        { text: '完成状态', value: 'is_finished' },
        //{ text: '已完成人数', value: 'dalaos' },
        { text: '更多', value: 'data-table-expand' },
      ],
      tags: [],
      ddls: [],
      expends: [],
      ////////////////////////////////////DDL列表 结束
      srcs: [],
      fileSubmit: {
        ftitle: '',
        furl: '',
        fpss: '',
      },

    }),

    //DDL列表 开始
    //DDL列表 结束


    created () {
      this.initialize()
    },

    methods: {
      initialize () {
        getUserCourses(this.$store.getters.uid).then(res => {
          console.log(res)
          var r_courses = res.courses;
          for (let i = 0; i < r_courses.length; i++) {
            this.tags.push(r_courses[i]);
          }
        })
      },
      chooseOne(item) {
        //alert("choose" + item.course_name);
        this.updatePage(item.cid);
      },
      updatePage (cid) {
        this.ddls = []
        getCourseByCid(this.$store.getters.uid, cid).then(res => {
          console.log(res)
          var r_tasks = res.tasks;
          for (let i = 0; i < r_tasks.length; i++) {
            this.ddls.push(r_tasks[i]);
          }
        })

        this.srcs = []
        getResourceByCid(this.$store.getters.uid, cid).then(res => {
          console.log(res)
          var r_resources = res.resources;
          for (let i = 0; i < r_resources.length; i++) {
            this.srcs.push(r_resources[i]);
          }
        })

        for (let i=0;i<this.ddls.length;i++) {
          this.courses[i] = this.ddls[i].name
          console.log(this.courses)
        }

        //DDL列表 开始
        //DDL列表 结束

      },

      getColor (remains) {
        if (remains < 20) return 'red'
        else if (remains < 100) return 'orange'
        else return 'green'
      },

      onFileSubmit() {
        this.$message('submit!' + this.fileSubmit);
        console.log(this.fileSubmit)
      }
    }
  }
</script>
