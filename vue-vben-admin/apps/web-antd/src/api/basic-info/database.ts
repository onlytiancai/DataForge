import { requestClient } from '#/api/request';

export namespace DemoTableApi {
  export interface PageFetchParams {
    [key: string]: any;
    page: number;
    pageSize: number;
  }
}


async function getDatabaseListApi(params: DemoTableApi.PageFetchParams) {
  return requestClient.get('/database/list', { params });
}

export { getDatabaseListApi };