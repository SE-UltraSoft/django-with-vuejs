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
                :expanded.sync="expanded"
                item-key="name"
              >
                <template v-slot:item.remains="{ item }">
                  <v-chip :color="getColor(item.remains)" dark>{{ item.remains }}</v-chip>
                </template>

                <template v-slot:item.glutenfree="{ item }">
                  <v-simple-checkbox v-model="item.glutenfree"></v-simple-checkbox>
                </template>

                <template v-slot:expanded-item="{ headers, item }">
                  <td :colspan="headers.length">{{ item.contents }}</td>
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
                      <th class="text-left">分享人</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in srcs" :key="item.name">
                      <td><a v-bind:href="item.url"> {{item.name}}</a></td>
                      <td v-if="item.pss!=''">{{ item.pss }}</td>
                      <td v-else></td>
                      <td>{{ item.sharer }}</td>
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
          value: 'name',
        },
        { text: '发布时间', value: 'starts' },
        { text: '截止时间', value: 'ends' },
        { text: '剩余时间', value: 'remains' },
        { text: '完成状态', value: 'glutenfree' },
        { text: '已完成人数', value: 'dalaos' },
        { text: '更多', value: 'data-table-expand' },
      ],
      ddls: [],
      ////////////////////////////////////DDL列表 结束
      tags: [],

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
          if (res.data.success) {
            var r_courses = res.data.courses;
            for (let i = 0; i < r_courses.data.length; i++) {
              this.tags.push(r_courses.data[i]);
            }
          }
        })
      },
      chooseOne(item) {
        alert("choose" + item.course_name);
        this.updatePage();
      },
      updatePage () {
        this.ddls = [
          {
            name: '计算机科学方法论',
            starts: 159,
            ends: 6.0,
            remains: 24,
            contacts: 4.0,
            glutenfree: false,
            dalaos: 22,
            contents: '计算机科学方法论作业具体内容',
          },
          {
            name: '软件工程（罗杰、任建）',
            starts: 237,
            ends: 9.0,
            remains: 200,
            contacts: 4.3,
            glutenfree: false,
            dalaos: 66,
            contents: '软件工程作业具体内容',
          },
        ]
        this.srcs = [
          {
            name: '计算机网络课程笔记',
            url: 'https://www.buaa.edu.cn',
            pss: '',
            sharer: '小小软',
          },
          {
            name: '软件工程学习资料',
            url: 'https://pan.baidu.com',
            pss: '2020',
            sharer: '大大软',
          },
        ]
        var i
        for (i=0;i<this.ddls.length;i++) {
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
