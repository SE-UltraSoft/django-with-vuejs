import request from '@/utils/request'

export function getAllTasks(params) {
  return request({
    url: '/api/user/uid/tasks',
    method: 'get',
    params
  })
}

/*
export function deleteOneTask(data) {
  console.log('delete task:')
  console.log(data)
  return request({
    url: '/vue-admin-template/tasks/deleteOne',
    method: 'post',
    data
  })
}
*/
export function createOneTask(data) {
  console.log('create a new task:')
  console.log(data)
  return request({
    url: '/api/user/uid/tasks/new',
    method: 'post',
    data
  })
}

export function modifyOneTask(data) {
  console.log('modify task:')
  console.log(data)
  return request({
    url: '/api/user/uid/tasks/modify',
    method: 'post',
    data
  })
}
