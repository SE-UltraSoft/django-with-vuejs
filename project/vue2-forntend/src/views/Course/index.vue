<template>
  <div class="app-container">
    <v-app>
      <v-row class="fill-height">
        <v-container fluid>
          <!--v-col-->
            <v-chip-group
              column
                active-class="primary--text"
              >
                <v-chip v-for="tag in tags" :key="tag.cid" @click="chooseOne(tag)" 
                  class="ma-2" color="blue" outlined label
                >
                  {{ tag.name }}
                </v-chip>
            </v-chip-group>

            <!--v-combobox
              v-model="select"
              :items="courses"
              label="已选课程"
              multiple
              chips
              dense
            ></v-combobox-->
          <!--/v-col-->
          <v-tabs>
            <v-tab>DDL列表</v-tab>
            <v-tab>共享资源</v-tab>

            <!--DDL列表 开始-->
            <v-tab-item>
              <v-data-table
                :headers="headers"
                :items="tasks"
                sort-by="ddl_time"
                :search="search"
              >
                <template v-slot:top>
                  <v-toolbar flat color="white">
                    <v-text-field
                      v-model="search"
                      append-icon="mdi-magnify"
                      label="Search"
                      single-line
                      hide-details
                      class="mr-12"
                    ></v-text-field>

                    <v-dialog v-model="dialog" max-width="500px">
                      <template v-slot:activator="{ on }">
                        <v-btn color="primary" dark class="mb-2" v-on="on">创建新日程</v-btn>
                      </template>
                      <v-card>
                        <v-card-title>
                          <span class="headline">{{ formTitle }}</span>
                        </v-card-title>

                        <v-card-text>
                          <v-container>
                            <v-row>
                              <v-col cols="12" sm="6" md="4">
                                <v-text-field v-model="editedItem.name" label="事项名称"></v-text-field>
                              </v-col>
                              <v-col cols="12" sm="6" md="4">
                                <v-text-field v-model="editedItem.start_time" label="发布时间"></v-text-field>
                              </v-col>
                              <v-col cols="12" sm="6" md="4">
                                <v-text-field v-model="editedItem.ddl_time" label="截止时间"></v-text-field>
                              </v-col>
                              <v-col cols="12" sm="6" md="4">
                                <v-text-field v-model="editedItem.remain" label="剩余时间"></v-text-field>
                              </v-col>
                              <v-col cols="12" sm="6" md="4">
                                <v-text-field v-model="editedItem.done" label="完成状态"></v-text-field>
                              </v-col>
                            </v-row>
                          </v-container>
                        </v-card-text>

                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
                          <v-btn color="blue darken-1" text @click="save">Save</v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                  </v-toolbar>
                </template>
                <!--完成状态复选框-->
                <template v-slot:item.done="{ item }">
                    <v-simple-checkbox v-model="item.done" ></v-simple-checkbox>
                </template>
                <template v-slot:item.actions="{ item }">
                  <v-icon
                    small
                    class="mr-2"
                    @click="editItem(item)"
                  >
                    mdi-pencil
                  </v-icon>
                  <v-icon
                    small
                    @click="deleteItem(item)"
                  >
                    mdi-delete
                  </v-icon>
                </template>
                <template v-slot:no-data>
                  <v-btn color="primary" @click="initialize">Reset</v-btn>
                </template>
              </v-data-table>
            </v-tab-item>
            <!--DDL列表 结束-->

            <v-tab-item>
              <v-simple-table >
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th class="text-left">资源名称</th>
                      <th class="text-left">资源链接</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in courseSrc" :key="item.name">
                      <td>{{ item.name }}</td>
                      <td>{{ item.url }}</td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>


              <v-divider></v-divider>

              <v-col>
                <el-form :inline="true" :model="downloadInline" class="demo-form-inline">
                  <el-form-item label="文件名">
                    <el-input v-model="downloadInline.ftitle" placeholder="文件名"></el-input>
                  </el-form-item>
                  <el-form-item label="分享链接">
                    <el-input v-model="downloadInline.furl" placeholder="分享链接"></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" :disabled="!(downloadInline.furl&&downloadInline.ftitle)" @click="onFileSubmit">分享</el-button>
                  </el-form-item>
                </el-form>
              </v-col>

            </v-tab-item>
          </v-tabs>
        </v-container>


      </v-row>
    </v-app>
  </div>
</template>

<script>
  //DDL列表 开始
  var  responseL={
      "success": true,
      "message": "Success.",
      "user": {
          "uid": 1,
          "student_id": "17373001",
          "name": "北小航",
          "email": "0000001@qq.com"
     },
      "data": [ //这里的data是task集合
          { // homework
              "tid": 27,
              "title": "团队博客——功能规格",
              "category": "homework",
              "content": "这是一篇团队博客",
              "useful_urls": [
                  "www.edu.cnblogs.com/xxxxx",
                  "www.github.com/BuaaRedSun/docs"
              ],
              "cid": "BH000001",
              "ddl": {
                  "ddl_id": 13,
                  "ddl_time": {
                      "date": "2020-04-21",
                      "time": "23:55"
                  },
                  "notification_time": {
                      "date": "2020-04-20",
                      "time": "23:55",
                      "repeat": null
                  },
                  "notification_content": "交作业啦"
              }
          },
          { // exam
              "tid": 35,
              "title": "工科数学分析期中考试",
              "category": "exam",
              "useful_urls": null,
              "cid": "BH0000102",
              "ddl": {
                  "ddl_id": 30,
                  "ddl_time": {
                      "date": "2020-04-22",
                      "time": "14:30"
                  },
                  "notification_time": {
                      "date": "2020-06-15",
                      "time": "08:00",
                      "repeat": "day"
                  },
                  "notification_content": "淑芬考试"
              }
          },
          { // personal
              "tid": 42,
              "title": "拿快递",
              "category": "personal",
              "useful_urls": null,
              "cid": null,
              "ddl": {
                  "ddl_id": 50,
                  "ddl_time": {
                      "date": "2020-04-18",
                      "time": "17:30"
                  },
                  "notification_time": {
                      "date": "2020-04-18",
                      "time": "17:00",
                      "repeat": null
                  },
                  "notification_content": "东门顺丰快递"
              }
          },
          { // meeting
              "tid": 77,
              "title": "志愿者例会",
              "category": "meeting",
              "useful_urls": [
                  "www.bv2008.cn"
              ],
              "cid": null,
              "ddl": {
                  "ddl_id": 70,
                  "ddl_time": {
                      "date": "2020-05-01",
                      "time": "14:30"
                  },
                  "notification_time": {
                      "date": "2020-05-01",
                      "time": "14:00",
                      "repeat": "week"
                  },
                  "notification_content": "汇报周进展"
              }
          },
      ]
  }

  //DDL列表 结束

var responseC = {
  data:[
    {
      name:'软工',
      cid:1,
    },
    {
      name:'计网',
      cid:2,
    }

  ]
  }

  export default {
    data: () => ({
      //课程组合框 开始
      select: [],
      courses: [],
      ddls: [],
      //课程组合框 结束

      ////////////////////////////////////DDL列表 开始
      dialog: false,
      search: '',
      headers: [
        {
          text: '事项名称',
          align: 'start',
          sortable: false,
          value: 'name',
        },
        { text: '发布时间', value: 'start_time' },
        { text: '截止日期', value: 'ddl_time' },
        { text: '剩余时间', value: 'remain' },
        { text: '完成状态', value: 'done' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      tasks: [],
      editedIndex: -1,
      editedItem: {
        name: '',
        start_time: '',
        ddl_time: '',
        doen: ''
      },
      defaultItem: {
        name: '',
        start_time: '',
        ddl_time: '',
        doen: ''
      },
      ////////////////////////////////////DDL列表 结束


      courseSrc: [],
      downloadInline: {
        ftitle: '',
        furl: ''
      },

      tags: []


    }),

    //DDL列表 开始
    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
      },
    },
    watch: {
      dialog (val) {
        val || this.close()
      },
    },
    //DDL列表 结束


    created () {
      //this.initialize();
      this.initCourList();
    },

    methods: {
      //初始化已选课程
      initCourList(){
        //从后端获取课程信息 这边模拟的 var
        for(let i=0;i<responseC.data.length;i++){
            this.tags.push(responseC.data[i])
        }
      },
      chooseOne(item){
        alert("hahahah  "+item.cid);
        //item里面为你 tags里面某一项的对象的详细信息
        //这边向后台强求数据的时候会用到cid等数据
         //从后台获得相应的列表数据  然后初始化列表数据
         this.initialize();
         //然后课程资源也是一样的  你判断下当前的是哪个界面 不同界面请求不同数据 赋值不同变量
      },

      //图表编辑 开始
      initialize () {
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
        this.courseSrc = [
          {
            name: '计算机网络课程笔记',
            url: 'https://www.buaa.edu.cn',
          },
          {
            name: '软件工程学习资料',
            url: 'https://pan.baidu.com',
          },
        ]
        var i
        for (i=0;i<this.ddls.length;i++) {
          this.courses[i] = this.ddls[i].name
          console.log(this.courses)
        }

        //DDL列表 开始
        const temp=[]
          var rdata = responseL.data;
          for (let i = 0; i < rdata.length; i++){
            var ie = rdata[i]
            var ddl_etime = ie.ddl.ddl_time.date + ' ' + ie.ddl.ddl_time.time
            temp.push({
              name: ie.title,
              start_time: ddl_etime,
              ddl_time: ddl_etime,
              remain:'1h',
              doen: 'ture',
              datails:{
                tid:ie.tid,
              }
            })
          }
          this.tasks=temp;
          this.tasks[1].remain='1h 30min'
         },
         editItem (item) {
           this.editedIndex = this.tasks.indexOf(item)
           this.editedItem = Object.assign({}, item)
           this.dialog = true
         },
         deleteItem (item) {
           const index = this.tasks.indexOf(item)
           confirm('Are you sure you want to delete this item?') && this.tasks.splice(index, 1)
         },
         close () {
           this.dialog = false
           setTimeout(() => {
             this.editedItem = Object.assign({}, this.defaultItem)
             this.editedIndex = -1
           }, 300)
         },
         save () {
           if (this.editedIndex > -1) {
             Object.assign(this.tasks[this.editedIndex], this.editedItem)
           } else {
             this.tasks.push(this.editedItem)
           }
           this.close()
         },
        //DDL列表 结束

      },

      onFileSubmit() {
        this.$message('submit!' + this.downloadInline);
        console.log(this.downloadInline)
      }
    }

</script>
