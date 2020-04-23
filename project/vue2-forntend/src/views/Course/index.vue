<template>
  <div class="app-container">
    <v-app>
      <v-row class="fill-height">
        <v-rol>
          <!--课程组合框 开始-->
          <v-sheet height="100">
            <v-container fluid>
              <v-row>
                <v-col cols="12">
                  <v-combobox
                    v-model="select"
                    :items="items"
                    label="已选课程"
                    multiple
                    chips
                    dense
                  ></v-combobox>
                </v-col>
              </v-row>
            </v-container>
          </v-sheet>
          <!--课程组合框 结束-->

          <!--日程列表 开始-->
          <v-sheet height="100%">

            <el-tabs type="border-card">
              <el-tab-pane label="DDL列表">
                <v-data-table
                  :headers="headers"
                  :items="ddls"
                  :search="search"
                  sort-by="remains"
                  class="elevation-1"
                >

                  <!--自定义列 开始-->
                    <template v-slot:item.remains="{ item }">
                      <v-chip :color="getColor(item.remains)" dark>{{ item.remains }}</v-chip>
                    </template>
                  <!--自定义列 结束-->

                  <!--复选框 开始-->
                  <template v-slot:item.glutenfree="{ item }">
                    <v-simple-checkbox v-model="item.glutenfree" selectable></v-simple-checkbox>
                  </template>
                  <!--复选框 结束-->

                  <!--图表头部编辑 开始-->
                  <template v-slot:top>
                    <v-toolbar flat color="white">
                      <!--<v-toolbar-title>My CRUD</v-toolbar-title>
                      <v-divider
                        class="mx-4"
                        inset
                        vertical
                      ></v-divider>
                      <v-spacer></v-spacer>-->

                      <!--搜索框 开始-->
                      <v-text-field
                         v-model="search"
                         append-icon="mdi-magnify"
                         label="Search"
                         single-line
                         hide-details
                       ></v-text-field>
                       <!--搜索框 结束-->

                      <!--v-spacer></v-spacer-->

                      <!--图表编辑 开始-->
                      <v-dialog v-model="dialog" max-width="100%">
                        <!--template v-slot:activator="{ on }">
                          <v-btn color="primary" dark class="mb-2" v-on="on">New Item</v-btn>
                        </template-->
                        <v-card>
                          <v-card-title>
                            <span class="headline">{{ formTitle }}</span>
                          </v-card-title>

                          <v-card-text>
                            <v-container>
                              <v-row>
                                <v-col cols="12" sm="6" md="4">
                                  <v-text-field v-model="editedItem.name" label="Dessert name"></v-text-field>
                                </v-col>
                                <v-col cols="12" sm="6" md="4">
                                  <v-text-field v-model="editedItem.starts" label="Calories"></v-text-field>
                                </v-col>
                                <v-col cols="12" sm="6" md="4">
                                  <v-text-field v-model="editedItem.ends" label="Fat (g)"></v-text-field>
                                </v-col>
                                <v-col cols="12" sm="6" md="4">
                                  <v-text-field v-model="editedItem.remains" label="Carbs (g)"></v-text-field>
                                </v-col>
                                <v-col cols="12" sm="6" md="4">
                                  <v-text-field v-model="editedItem.contacts" label="Protein (g)"></v-text-field>
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
                      <!--图表编辑 结束-->
                    </v-toolbar>
                  </template>
                  <!--图表头部编辑 结束-->

                  <!--图表编辑 开始-->
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
                  <!--图表编辑 结束-->

                </v-data-table>

              </el-tab-pane>

              <el-tab-pane label="共享资源">

                <v-list>

                    <v-subheader>课程笔记</v-subheader>
                    <v-list-item @click="">
                      <v-list-item-action>
                        <v-icon>mdi-inbox-arrow-down</v-icon>
                      </v-list-item-action>
                      <v-list-item-content>
                        <v-list-item-title>I'm a list item</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>

                    <v-list-item @click="">
                      <v-list-item-action>
                        <v-icon>mdi-inbox-arrow-down</v-icon>
                      </v-list-item-action>
                      <v-list-item-content>
                        <v-list-item-title>I'm a list item</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>

                    <v-list-item @click="">
                      <v-list-item-action>
                        <v-icon>mdi-inbox-arrow-down</v-icon>
                      </v-list-item-action>
                      <v-list-item-content>
                        <v-list-item-title>I'm a list item</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>

                    <v-divider :inset="inset"></v-divider>

                    <v-subheader>资源文件</v-subheader>

                    <v-list-item @click="">
                      <v-list-item-action>
                        <v-icon>mdi-folder</v-icon>
                      </v-list-item-action>
                      <v-list-item-content>
                        <v-list-item-title>I'm a list item</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>

                    <v-divider :inset="inset"></v-divider>

                    <v-list-item @click="">
                      <v-list-item-action>
                        <v-icon>mdi-folder</v-icon>
                      </v-list-item-action>
                      <v-list-item-content>
                        <v-list-item-title>I'm a list item</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>

                    <v-divider :inset="inset"></v-divider>

                    <v-list-item @click="">
                      <v-list-item-action>
                        <v-icon>mdi-folder</v-icon>
                      </v-list-item-action>
                      <v-list-item-content>
                        <v-list-item-title>I'm a list item</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>

                <el-divider></el-divider>

                <el-form :inline="true" :model="downloadInline" class="demo-form-inline">
                  <el-form-item label="文件名">
                    <el-input v-model="downloadInline.ftitle" placeholder="文件名"></el-input>
                  </el-form-item>
                  <el-form-item label="分享链接">
                    <el-input v-model="downloadInline.furl" placeholder="分享链接"></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="onFileSubmit">分享</el-button>
                  </el-form-item>
                </el-form>

              </el-tab-pane>

            </el-tabs>

          </v-sheet>
          <!--日程列表 结束-->
        </v-rol>

      </v-row>
    </v-app>
  </div>
  </template>

<script>
  export default {
    data: () => ({
      //课程组合框 开始
      select: ['Vuetify', 'Programming'],
      items: [
        'Programming',
        'Design',
        'Vue',
        'Vuetify',
      ],
      //课程组合框 结束


      //日程表 开始
      search: '',
      dialog: false,
      headers: [
        {
          text: '任务',
          align: 'start',
          sortable: false,
          value: 'name',
        },
        { text: '开始时间', value: 'starts' },
        { text: '截止时间', value: 'ends' },
        { text: '剩余时间', value: 'remains' },
        { text: '联系人', value: 'contacts' },
        { text: '已完成', value: 'glutenfree' },
        { text: '编辑/删除', value: 'actions', sortable: false },

      ],
      ddls: [],
      editedIndex: -1,
      editedItem: {
        name: '',
        starts: 0,
        ends: 0,
        remains: 0,
        contacts: 0,
      },
      defaultItem: {
        name: '',
        starts: 0,
        ends: 0,
        remains: 0,
        contacts: 0,
      },
      //日程表 结束

      downloadInline: {
        ftitle: '',
        furl: ''
      }

    }),


    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
      },
    },

    watch: {
      //日程表 开始
      dialog (val) {
        val || this.close()
      },
      //日程表 结束

    },


    created () {
      this.initialize()
    },

    methods: {

      //自定义列 开始
      getColor (remains) {
        if (remains < 100) return 'red'
        else if (remains < 500) return 'orange'
        else return 'green'
      },
      //自定义列 结束


      //图表编辑 开始
      initialize () {
        this.ddls = [
          {
            name: 'Frozen Yogurt',
            starts: 159,
            ends: 6.0,
            remains: 24,
            contacts: 4.0,
            glutenfree: false,
          },
          {
            name: 'Ice cream sandwich',
            starts: 237,
            ends: 9.0,
            remains: 37,
            contacts: 4.3,
            glutenfree: false,
          },
          {
            name: 'Eclair',
            starts: 262,
            ends: 16.0,
            remains: 23,
            contacts: 6.0,
            glutenfree: false,
          },
          {
            name: 'Cupcake',
            starts: 305,
            ends: 3.7,
            remains: 670,
            contacts: 4.3,
            glutenfree: true,
          },
          {
            name: 'Gingerbread',
            starts: 356,
            ends: 16.0,
            remains: 495,
            contacts: 3.9,
            glutenfree: false,
          },
          {
            name: 'Jelly bean',
            starts: 375,
            ends: 0.0,
            remains: 194,
            contacts: 0.0,
            glutenfree: true,
          },
          {
            name: 'Lollipop',
            starts: 392,
            ends: 0.2,
            remains: 98,
            contacts: 0,
            glutenfree: false,
          },
          {
            name: 'Honeycomb',
            starts: 408,
            ends: 3.2,
            remains: 87,
            contacts: 6.5,
            glutenfree: true,
          },
          {
            name: 'Donut',
            starts: 452,
            ends: 25.0,
            remains: 51,
            contacts: 4.9,
            glutenfree: false,
          },
          {
            name: 'KitKat',
            starts: 518,
            ends: 26.0,
            remains: 65,
            contacts: 7,
            glutenfree: true,
          },
        ]
      },

      editItem (item) {
        this.editedIndex = this.ddls.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        const index = this.ddls.indexOf(item)
        confirm('Are you sure you want to delete this item?') && this.ddls.splice(index, 1)
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
          Object.assign(this.ddls[this.editedIndex], this.editedItem)
        } else {
          this.ddls.push(this.editedItem)
        }
        this.close()
      },
      //图表编辑 结束

      onFileSubmit() {
        this.$message('submit!');
        console.log(this.downloadInline)
      }

    },
  }
</script>
