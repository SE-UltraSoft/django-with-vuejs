import request from '@/utils/request'

export function getUserCourses(uid) {
  return request({
    url: '/user/${uid}/courses',
    method: 'get',
    uid
  })
}

export function getCourseByCid(uid, cid) {
  return request({
    url: '/user/${uid}/course/${cid}/tasks',
    method: 'get',
    uid,
    cid
  })
}

export function getResourceByCid(uid, cid) {
  return request({
    url: '/user/${uid}/course/${cid}/resources',
    method: 'get',
    uid,
    cid
  })
}
