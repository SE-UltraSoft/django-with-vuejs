<template>
  <div id="Calendar" class="app-container">
    <v-app>
      <v-row class="fill-height">
        <v-col>
          <v-sheet height="64">
            <v-toolbar flat color="white">
              <v-btn outlined class="mr-4" color="grey darken-2" @click="setToday">
                Today
              </v-btn>
              <v-btn fab text small color="grey darken-2" @click="prev">
                <v-icon small>mdi-chevron-left</v-icon>
              </v-btn>
              <v-btn fab text small color="grey darken-2" @click="next">
                <v-icon small>mdi-chevron-right</v-icon>
              </v-btn>
              <v-toolbar-title>{{ title }}</v-toolbar-title>
              <v-spacer></v-spacer>
              <v-select
                v-model="type"
                :items="types"
                dense
                outlined
                hide-details
                label="type"
                class="mr-10"
              ></v-select>
              <!-- 创建新事项弹窗-->
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
                    <v-btn color="blue darken-1" text @click="createTask('createForm')">立即创建</v-btn>
                    <v-btn color="blue darken-1" text @click="createCancel('createForm')">取消</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </v-sheet>
          <v-sheet height="600">
            <v-calendar
              ref="calendar"
              v-model="focus"
              color="primary"
              :events="events"
              :event-color="getEventColor"
              :now="today"
              :type="type"
              @click:event="showEvent"
              @click:more="viewDay"
              @click:date="viewDay"
              @change="updateRange"
            ></v-calendar>
            <!--事项详情页-->
            <v-dialog
              v-model="selectedOpen"
              :close-on-content-click="false"
              :activator="selectedElement"
              max-width="500px"
            >
              <v-card
                color="grey lighten-4"
                min-width="350px"
                flat
              >
                <v-toolbar
                  :color="selectedEvent.color"
                  dark
                >
                  <v-icon>mdi-pencil</v-icon>

                  <v-toolbar-title class="pl-2" v-html="selectedEvent.name"></v-toolbar-title>
                  <v-spacer></v-spacer>
                  <v-btn icon>
                    <v-icon
                      small
                      @click="deleteItem(selectedEvent)"
                    >
                      mdi-delete
                    </v-icon>
                  </v-btn>
                </v-toolbar>
                <v-card-text >
                  <p></p>
                  <el-form ref="form" :model="form" label-width="100px">
                    <el-form-item label="截止时间">
                      <span v-text="form.ddlTime"></span>
                    </el-form-item>
                    <el-form-item label="发布时间">
                      <span v-text="form.startTime"></span>
                    </el-form-item>
                    <el-form-item label="事项分类">
                      <span v-text="form.type"></span>
                    </el-form-item>
                    <el-form-item v-if="form.type=='homework'" label="关联课程">
                      <span v-text="form.course"></span>
                    </el-form-item>
                    <el-form-item v-if="form.type=='homework'" label="提交平台">
                      <span v-text="form.platform"></span>
                    </el-form-item>
                    <el-form-item label="完成状态">
                      <el-switch v-model="form.done" active-color="#13ce66"></el-switch>
                    </el-form-item>
                    <el-form-item label="开启提醒功能">
                      <el-switch v-model="form.alert"></el-switch>
                    </el-form-item>
                    <el-form-item label="提醒时间">
                      <el-date-picker
                            v-model="form.alertTime"
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
                  <v-btn color="blue darken-1" text @click="modifyTaskSave(selectedEvent)">保存修改</v-btn>
                  <v-btn color="blue darken-1" text @click="selectedOpen = false">取消</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-sheet>
        </v-col>
      </v-row>
    </v-app>
  </div>
</template>

<script>
import { getAllTasks, deleteOneTask,createOneTask,modifyOneTask } from "@/api/tasks"

export default {
  name:'Calendar',
  data: () => ({
    focus: '',
    type: 'month',
    types: ['month', 'week', 'day', '4day'],
    start: null,
    end: null,
    selectedEvent: {},
    selectedElement: null,
    selectedOpen: false, //事项详情窗口的开关状态
    createOpen: false, //创建日程窗口的开关状态
    events: [],
    colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1'],
    names: ['Meeting', 'Holiday', 'PTO', 'Travel', 'Event', 'Birthday', 'Conference', 'Party'],
    form:{
        name: '',
        startTime: '',
        ddlTime: '',
        type: '',//事件分类
        platform:'',
        course: '',
        done: false,
        alert: true,
        alertTime: ''
      },
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
    title() {
      const { start, end } = this
      if (!start || !end) {
        return ''
      }
      const startMonth = this.monthFormatter(start)
      const endMonth = this.monthFormatter(end)
      const suffixMonth = startMonth === endMonth ? '' : endMonth
      const startYear = start.year
      const endYear = end.year
      const suffixYear = startYear === endYear ? '' : endYear
      const startDay = start.day + this.nth(start.day)
      const endDay = end.day + this.nth(end.day)
      switch (this.type) {
        case 'month':
          return `${startMonth} ${startYear}`
        case 'week':
        case '4day':
          return `${startMonth} ${startDay} ${startYear} - ${suffixMonth} ${endDay} ${suffixYear}`
        case 'day':
          return `${startMonth} ${startDay} ${startYear}`
      }
      return ''
    },
    monthFormatter() {
      return this.$refs.calendar.getFormatter({
        timeZone: 'UTC', month: 'long',
      })
    }
  },
  mounted() {
    this.$refs.calendar.checkChange()
  },
  created () {
    getAllTasks().then(res => {  // fetch data
        // return response
        console.log(res)
        this.initialize(res.data)
    })
  },
  methods: {
    viewDay({ date }) {
      this.focus = date
      this.type = 'day'
    },
    getEventColor(event) {
      return event.color
    },
    setToday() {
      this.focus = this.today
    },
    prev() {
      this.$refs.calendar.prev()
    },
    next() {
      this.$refs.calendar.next()
    },
    showEvent({ nativeEvent, event }) {
      const open = () => {
        this.selectedEvent = event
        this.selectedElement = nativeEvent.target
        setTimeout(() => this.selectedOpen = true, 10)
        //详情展示
        this.form.ddlTime = event.start;
        this.form.startTime = event.detail.created_at;
        this.form.type = event.detail.category;
        this.form.done= event.detail.is_finished;
        this.form.alert = event.detail.ddl.notification_alert;
        this.form.alertTime = event.detail.ddl.notification_time;
        this.form.course=event.detail.course_name;
        this.form.platform=event.detail.platform;
      }
      if (this.selectedOpen) {
        this.selectedOpen = false
        setTimeout(open, 10)
      } else {
        open()
      }
      nativeEvent.stopPropagation()
    },
    setColor(type){
        if(type ==='homework')
            return 'orange'
        else if(type ==='exam')
            return 'red'
        else if(type ==='meeting')
            return 'green'
        else if(type ==='personal')
            return 'blue'
        else
            return 'blue'
    },
    updateRange({ start, end }) {
      this.start = start
      this.end = end
    },
    initialize(fetched_data) {
      var events = []
      console.log(fetched_data.data)
      var rdata = fetched_data.data
      for (let i = 0; i < rdata.length; i++){
          var ie = rdata[i]
          events.push({
            name: ie.title,
            start: ie.ddl.ddl_time,
            color: this.setColor(ie.category),
            detail: ie     //保存此task的全部信息
          })
        }
      console.log(events.length)

      this.events = events
      console.log(this.events)
    },
    deleteItem(event) {
      const index = this.events.indexOf(event)
      confirm('Are you sure you want to delete this item?') && this.events.splice(index, 1)
      console.log(event)
      this.selectedOpen = false
      //与后端交互 删除task
      deleteOneTask(event.detail).then(res => {
        console.log(res.data)
      })
    },
    createTask(formName){
      this.$refs[formName].validate((valid) => {
                var temp = this.createForm;
                const ddl_date_time = this.createForm.ddlDay+' '+this.createForm.ddlTime;
                const alert_date_time=this.createForm.alertDay+' '+this.createForm.alertTime;
                const detail=this.formatDetail(-1,temp.name,temp.type,null,temp.platform,-1,temp.course,-1,
                                           ddl_date_time,temp.alert,alert_date_time,this.formatDate(new Date(),true),false)
                if (valid) {
                  var newEvent={
                    name:this.createForm.name,
                    start:ddl_date_time,
                    color:this.setColor(this.createForm.type),
                    detail:detail
                    }
                  this.events.push(newEvent);
                  // 与后端交互 创建新task
                  createOneTask(detail).then(res =>{
                    console.log(res.data)
                  })
                  this.$refs[formName].resetFields();
                  this.createOpen = false;
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
    modifyTaskSave(event){
      //与后端交互  修改task
      event.detail.is_finished=this.form.done;
      event.detail.ddl.notification_alert=this.form.alert;
      event.detail.ddl.notification_time=this.form.alertTime ;
      console.log(event.detail)
      console.log(this.selectedEvent)
      console.log(this.form)
      modifyOneTask(event.detail).then(res =>{
      console.log(res.data)
      this.selectedOpen=false
      })
     },
    nth(d) {
      return d > 3 && d < 21
        ? 'th'
        : ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'][d % 10]
    },
    rnd(a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a
    },
    formatDate(a, withTime) {
      return withTime
        ? `${a.getFullYear()}-${a.getMonth() + 1}-${a.getDate()} ${a.getHours()}:${a.getMinutes()}:${a.getSeconds()}`
        : `${a.getFullYear()}-${a.getMonth() + 1}-${a.getDate()}`
    },

    //生成detail格式，与从后台获取的json中的data格式相同
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
        return detail;
    }
  }
}
</script>
