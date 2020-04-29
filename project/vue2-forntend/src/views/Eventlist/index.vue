<template>
  <div id ="Eventlist">
  <v-app>
    <v-data-table
      :headers="headers"
      :items="tasks"
      sort-by="ddl_time"
      class="elevation-1 mx-5"
      :search="search"
    >
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title>ddl列表</v-toolbar-title>
          <v-divider
            class="mx-4"
            inset
            vertical
          ></v-divider>
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            single-line
            hide-details
            class="mr-12"
          ></v-text-field>
          <v-dialog v-model="createOpen" max-width="500px">
            <template v-slot:activator="{ on }">
              <v-btn color="primary" dark class="mb-2" v-on="on">创建新日程</v-btn>
            </template>
            <v-card>
              <v-toolbar color="primary" dark>
                <v-toolbar-title>创建新日程</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <p></p>
                <el-form ref="createForm" :model="createForm" :rules="createRule" label-width="110px">
                  <el-form-item label="事项名称" prop="name">
                    <el-input v-model="createForm.name"></el-input>
                  </el-form-item>
                  <el-form-item label="事项类型">
                    <el-select v-model="createForm.type" placeholder="请选择类型">
                      <el-option label="个人" value="personal"></el-option>
                      <el-option label="作业" value="homework"></el-option>
                      <el-option label="会议" value="meeting"></el-option>
                      <el-option label="考试" value="exam"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="关联课程" v-if="createForm.type=='homework'">
                    <el-input v-model="createForm.course"></el-input>
                  </el-form-item>
                  <el-form-item label="相关平台" v-if="createForm.type=='homework'">
                    <el-input v-model="createForm.platform"></el-input>
                  </el-form-item>
                  <el-form-item label="截止时间">
                    <el-col :span="11">
                      <el-form-item prop="ddlDay">
                        <el-date-picker  value-format="yyyy-MM-dd" format="yyyy-MM-dd" placeholder="选择日期"  v-model="createForm.ddlDay" style="width: 100%;"></el-date-picker>
                      </el-form-item>
                    </el-col>
                    <el-col class="line" :span="2">-</el-col>
                    <el-col :span="11">
                      <el-form-item prop="ddlTime">
                        <el-time-picker value-format="HH:mm:ss" format="HH:mm:ss" placeholder="选择时间" v-model="createForm.ddlTime" style="width: 100%;"></el-time-picker>
                      </el-form-item>
                    </el-col>
                  </el-form-item>
                  <el-form-item label="开启提醒" prop="alert">
                    <el-switch v-model="createForm.alert"></el-switch>
                  </el-form-item>
                  <el-form-item label="提醒时间" v-if="createForm.alert==true">
                    <el-col :span="11">
                      <el-form-item prop="alertDay">
                        <el-date-picker  value-format="yyyy-MM-dd" format="yyyy-MM-dd" placeholder="选择日期" v-model="createForm.alertDay" style="width: 100%;"></el-date-picker>
                      </el-form-item>
                    </el-col>
                    <el-col class="line" :span="2">-</el-col>
                    <el-col :span="11">
                      <el-form-item prop="alertTime">
                        <el-time-picker value-format="HH:mm:ss" format="HH:mm:ss" placeholder="选择时间" v-model="createForm.alertTime" style="width: 100%;"></el-time-picker>
                      </el-form-item>
                    </el-col>
                  </el-form-item>
                  <el-form-item label="是否提醒他人" v-if="createForm.type!=personal" prop="alertOther">
                    <el-switch v-model="createForm.alertOther"></el-switch>
                  </el-form-item>
                  <el-form-item v-if="createForm.alertOther==true" label="事项相关成员" prop="remindValue">
                    <el-select
                        v-model="createForm.remindValue"
                        multiple
                        filterable
                        allow-create
                        default-first-option
                        placeholder="请输入学号">
                      </el-select>
                  </el-form-item>
                </el-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text v-on="on" @click="createTask('createForm')">立即创建</v-btn>
                <v-btn color="blue darken-1" text @click="createCancel('createForm')">取消</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <!--完成状态复选框-->
      <template v-slot:item.done="{ item }">
          <v-simple-checkbox v-model="item.done" disabled></v-simple-checkbox>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2"  @click="editItem(item)"> mdi-pencil </v-icon>
        <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
        <v-dialog v-model="editOpen" max-width="500px">
          <v-card>
            <v-card-title>
              <span class="headline" v-text="editedItem.name"></span>
            </v-card-title>
            <v-card-text>
                <p></p>
                <el-form ref="editedItem" :model="editedItem" label-width="100px">
                  <el-form-item label="发布时间">
                    <span v-text="editedItem.start_time"></span>
                  </el-form-item>
                  <el-form-item label="截止时间">
                    <span v-text="editedItem.ddl_time"></span>
                  </el-form-item>
                  <el-form-item label="事项分类">
                    <span v-text="editedItem.category"></span>
                  </el-form-item>
                  <el-form-item v-if="editedItem.category=='homework'" label="关联课程">
                    <span v-text="editedItem.cname"></span>
                  </el-form-item>
                  <el-form-item v-if="editedItem.category=='homework'" label="提交平台">
                    <span v-text="editedItem.platform"></span>
                  </el-form-item>
                  <el-form-item label="完成状态">
                    <el-switch v-model="editedItem.done" active-color="#13ce66"></el-switch>
                  </el-form-item>
                  <el-form-item label="开启提醒功能">
                    <el-switch v-model="editedItem.alert"></el-switch>
                  </el-form-item>
                  <el-form-item label="提醒时间">
                    <el-date-picker
                          v-model="editedItem.alert_time"
                          type="datetime"
                          placeholder="选择日期时间"
                          value-format="yyyy-MM-dd HH:mm:ss"
                          format="yyyy-MM-dd HH:mm:ss"
                          default-time="12:00:00">
                        </el-date-picker>
                  </el-form-item>
                </el-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="modifyTaskSave(item)">保存修改</v-btn>
                <v-btn color="blue darken-1" text @click="editOpen = false">取消</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
      </template>

      <template v-slot:no-data>
        <v-btn color="primary" @click="initialize">Reset</v-btn>
      </template>
    </v-data-table>
  </v-app>
 </div>
</template>

<script>
import { getAllTasks, deleteOneTask, createOneTask, modifyOneTask } from "@/api/tasks"

export default {
    data: () => ({
      editOpen: false,//详情页
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
        { text: '事项类型', value: 'category' },
        { text: '完成状态', value: 'done' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      tasks: [],
      editedIndex: -1,
      defaultItem: {
        name:'',
        start_time:'',
        ddl_time:'',
        category:'',
        cname:'',
        platform:'',
        doen:false,
        alert:false,
        alert_time:'',
        datails:null
      },
      editedItem:{
        name:'',
        start_time:'',
        ddl_time:'',
        category:'',
        cname:'',
        platform:'',
        doen:false,
        alert:false,
        alert_time:'',
        datails:null
      },
      createOpen:false,//创建界面
      createForm: {
          name: '',
          type: "personal",
          course:'',
          platform:'',
          ddlDay: '',
          ddlTime: '',
          alert: false,
          alertDay:'',
          alertTime:'',
          alertOther: false,
          remindValue: []
        },
      createRule:{
        name:[
           { required: true, message: '请输入事项名称', trigger: 'blur' },
        ],
        ddlDay:[
          { required: true, message: '请选择日期', trigger: 'change' }
        ],
        ddlTime:[
          {  required: true, message: '请选择时间', trigger: 'change' },
        ],
        alertDay:[
          {  required: true, message: '请选择日期', trigger: 'change' }
        ],
        alertTime:[
          {  required: true, message: '请选择时间', trigger: 'change' },
        ],
        remindValue: [
          { type: 'array', required: true, message: '请至少输入一个学号', trigger: 'change' }
        ],
      }
    }),
    computed: {
    },
    watch: {
      dialog (val) {
        val || this.close()
      },
    },
    created () {
      getAllTasks().then(res => {  // fetch data
          // return response
          console.log(res)
          this.initialize(res.data)
      })
    },
    methods: {
      initialize(fetched_data) {
        const temp = []
        var rdata = fetched_data.data
        // var rdata = responseL.data;
        // var rdata = fetchData()
        for (let i = 0; i < rdata.length; i++){
          var ie = rdata[i]
          temp.push({
            name: ie.title,
            start_time: ie.created_at,
            ddl_time: ie.ddl.ddl_time,
            category:ie.category,
            cname:ie.course_name,
            platform:ie.platform,
            doen: ie.is_finished,
            alert:ie.ddl.notification_alert,
            alert_time:ie.ddl.notification_time,
            datails:ie,
          })
        }
        this.tasks= temp;
      },
      editItem(item) {
        this.editedIndex = this.tasks.indexOf(item)
        console.log(this.editedIndex)
        //给editItem赋值
        this.editedItem = Object.assign({}, item)
        console.log(this.editedItem)
        //this.editedItem.detail=Object.assign({},item.detail)
        this.editOpen = true
        console.log(this.editOpen)
      },
      modifyTaskSave(item){
        Object.assign(this.tasks[this.editedIndex], this.editedItem)
        this.editOpen=false
        modifyOneTask(item.detail).then(res =>{
          console.log(res.data)
        })
      },
      deleteItem(item) {
        const index = this.tasks.indexOf(item)
        confirm('Are you sure you want to delete this item?') && this.tasks.splice(index, 1)
        //与后端交互 删除task
        deleteOneTask(item.detail).then(res => {
          console.log(res.data)
        })
      },
      createTask(formName){
        this.$refs[formName].validate((valid) => {
                  var temp = this.createForm;
                  const ddl_date_time = this.createForm.ddlDay+' '+this.createForm.ddlTime;
                  const alert_date_time=this.createForm.alertDay+' '+this.createForm.alertTime;
                  const create_time = this.formatDate(new Date(),true);
                  const detail=this.formatDetail(-1,temp.name,temp.type,null,temp.platform,-1,temp.course,-1,
                                             ddl_date_time,temp.alert,alert_date_time,create_time,false)
                  if (valid) {
                    var newTask={
                      name: temp.name,
                      start_time:create_time ,
                      ddl_time: ddl_date_time,
                      category:temp.type,
                      cname:temp.course,
                      platform:temp.platform,
                      doen:temp.done,
                      alert:temp.alert,
                      alert_time:alert_date_time,
                      detail:detail
                      }
                    this.tasks.push(newTask);
                    this.createOpen = false;
                    // 与后端交互 创建新task
                    console.log(temp.remindValue)
                    createOneTask(detail).then(res =>{
                      console.log(res.data)
                    })
                    this.$refs[formName].resetFields();

                  } else {
                    console.log('error submit!!');
                    return false;
                  }
                });
      },
      createCancel(formName){
        this.$refs[formName].resetFields();
        this.createOpen = false
      },
      formatDate(a, withTime) {
        return withTime
          ? `${a.getFullYear()}-${a.getMonth() + 1}-${a.getDate()} ${a.getHours()}:${a.getMinutes()}:${a.getSeconds()}`
          : `${a.getFullYear()}-${a.getMonth() + 1}-${a.getDate()}`
      },
      formatDetail(tid,title,category,urls,platform,cid,cname,ddl_id,ddl_time,alert,alert_time,create_time,done){
        var detail = { // personal
            "tid":tid,
            "title":title,
            "category": category,
            "useful_urls": null,
            "platform": platform,
            "cid": null,
            "course_name": cname,
            "ddl": {
                "ddl_id":ddl_id,
                "ddl_time":ddl_time,
                "notification_alert":alert,
                "notification_time":alert_time,
                "notification_repeat": null,
                "notification_content": ''
            },
            "created_at":create_time, //获取时间
            "is_finished": done
          }
          return detail
      }
    }
  }
</script>
