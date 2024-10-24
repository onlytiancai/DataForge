import type { RouteRecordRaw } from 'vue-router';

import { BasicLayout } from '#/layouts';
import { $t } from '#/locales';

const routes: RouteRecordRaw[] = [
  {
    component: BasicLayout,
    meta: {
      icon: 'ic:baseline-view-in-ar',
      keepAlive: true,
      order: 1000,
      title: $t('test.title'),
    },
    name: 'Test',
    path: '/test',
    children: [
      {
        meta: {
          title: $t('test.export-csv'),
        },
        name: 'TestTest',
        path: '/test/test',
        component: () => import('#/views/test/index.vue'),
      },
    ],
  },
];

export default routes;
