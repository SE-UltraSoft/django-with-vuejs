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
                  <v-card-title>
                    <span class="headline">fmh小朋友的秀场</span>
                  </v-card-title>
                  <v-card-text>
                    <v-container>
                     <p>瑞斯拜</p>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="createOpen = false">取消</v-btn>
                    <v-btn color="blue darken-1" text @click="createTaskSave">保存</v-btn>
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
                  <el-form ref="form" :model="form" label-width="100px" >
                    <el-form-item label="截止时间">
                      <span v-text="form.ddlTime"></span>
                    </el-form-item>
                    <el-form-item label="发布时间">
                      <span v-text="form.startTime"></span>
                    </el-form-item>
                    <el-form-item label="事项分类">
                      <span v-text="form.type"></span>
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
                            default-time="12:00:00">
                          </el-date-picker>
                    </el-form-item>
                  </el-form>
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="selectedOpen = false">取消</v-btn>
                  <v-btn color="blue darken-1" text @click="updateTaskSave">保存</v-btn>
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
var  responseL={
    "success": true,
    "message": "Success.",
    "uid": 1,
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
            "platform": "博客园",
            "cid": "1",
            "course_name": "软件工程",
            "ddl": {
                "ddl_id": 13,
            "ddl_time": "2020-04-10 23:55:00",
                "notification_alert": true,
            "notification_time": "2020-04-09 23:55:00",
            "notification_repeat": null,
            "notification_content": "交作业啦"
            },
            "created_at": "2020-03-20 15:33:20",
            "is_finished": false
        },
        { // exam
            "tid": 35,
            "title": "工科数学分析期中考试",
            "category": "exam",
            "useful_urls": [], //集合size=1即可，空值有点奇怪
            "platform": "教4-401",
            "cid": "3",
            "course_name": "工科数学分析",
            "ddl": {
                "ddl_id": 30,
                "ddl_time": "2020-04-29 14:30:00",
                "notification_alert": false,
                "notification_time": "2020-04-29 14:30:00",
                "notification_repeat": "day",
                "notification_content": "淑芬考试",
            },
            "created_at": "2020-03-20 15:33:20",
            "is_finished": false
        },
        { // personal
            "tid": 42,
            "title": "拿快递",
            "category": "personal",
            "useful_urls": null,
            "platform": null,
            "cid": null,
            "course_name": null,
            "ddl": {
                "ddl_id": 50,
                "ddl_time": "2020-04-20 17:30:00",
                "notification_alert": true,
                "notification_time": "2020-04-11 17:00",
                "notification_repeat": null,
                "notification_content": "东门顺丰快递"
            },
            "created_at": "2020-03-20 15:33:20",
            "is_finished": true
        },
        { // meeting
            "tid": 77,
            "title": "志愿者例会",
            "category": "meeting",
            "useful_urls": [
                "www.bv2008.cn"
            ],
            "platform": "志愿北京",
            "cid": "1",
            "course_name": null,
            "ddl": {
                "ddl_id": 70,
                "ddl_time": "2020-04-23 14:30:00",
                "notification_alert": true,
                "notification_time": "2020-04-01 14:00:00",
                "notification_repeat": "week",
                "notification_content": "汇报周进展"
            },
            "created_at": "2020-03-20 15:33:20",
            "is_finished": false
        },
    ]
}

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
        name:'',
        startTime:'',
        ddlTime:'',
        type:'',//事件分类
        platform:'',
        course:'',
        done:false,
        alert:true,
        alertTime:''
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
        this.form.done=event.detail.is_finished;
        this.form.alert = event.detail.ddl.notification_alert;
        this.form.alertTime = event.detail.ddl.notification_time;
        
      }
      if (this.selectedOpen) {
        this.selectedOpen = false
        setTimeout(open, 10)
      } else {
        open()
      }
      nativeEvent.stopPropagation()
    },
    updateRange({ start, end }) {
      const events = []
      /*
      const min = new Date(`${start.date}T00:00:00`)
      const max = new Date(`${end.date}T23:59:59`)
      const days = (max.getTime() - min.getTime()) / 86400000
      //随机生成event

      const eventCount = this.rnd(days, days + 20)
      for (let i = 0; i < eventCount; i++) {
        const allDay = this.rnd(0, 3) === 0
        const firstTimestamp = this.rnd(min.getTime(), max.getTime())
        const first = new Date(firstTimestamp - (firstTimestamp % 900000))
        const secondTimestamp = this.rnd(2, allDay ? 288 : 8) * 900000
        const second = new Date(first.getTime() + secondTimestamp)
        events.push({
          name: this.names[this.rnd(0, this.names.length - 1)],
          start: this.formatDate(first, !allDay),
          end: this.formatDate(second, !allDay),
          color: this.colors[this.rnd(0, this.colors.length - 1)]
        })
        */
      //为不同类型分配颜色
      const setColor = (type)=>  {
          if(type ==='homework')
              return 'orange'
          else if(type ==="exam")
              return 'red'
          else if(type ==='meeting')
              return 'green'
          else if(type ==='personal')
              return 'blue'
          else
              return 'blue'
      }

       //与后端交互  获得用户的全部tasks
      if (responseL.success == true){ //成功查询返回
        const rdata = responseL.data;
        for (let i = 0; i < rdata.length; i++){
          var ie = rdata[i]
          events.push({
            name: ie.title,
            start: ie.ddl.ddl_time,
            color: setColor(ie.category),
            detail: ie     //保存此task的全部信息
          })
        }
      }
      this.start = start
      this.end = end
      this.events = events
    },
    deleteItem(event) {
      const index = this.events.indexOf(event)
      confirm('Are you sure you want to delete this item?') && this.events.splice(index, 1)
      console.log(this.events)
      this.selectedOpen = false
      //与后端交互 删除task
    },
    createTaskSave(){
      this.createOpen = false
      // 与后端交互 创建新task
    },
    updateTaskSave(event){
      this.selectedOpen=false
      //与后端交互  修改task
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
        ? `${a.getFullYear()}-${a.getMonth() + 1}-${a.getDate()} ${a.getHours()}:${a.getMinutes()}`
        : `${a.getFullYear()}-${a.getMonth() + 1}-${a.getDate()}`
    }
  }
}
</script>
