import request from '@/utils/request'

export function getUserCourses(uid) {
  return request({
    url: '/vue-admin-template/api/user/courses',
    method: 'get',
    params: { uid }
  })
}