import service from '@/utils/request'

// 搜索URL
export function searchUrlA(url) {
  return service({
    url: "/website/get_links/" + url,
    method: 'get'
  })
}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        