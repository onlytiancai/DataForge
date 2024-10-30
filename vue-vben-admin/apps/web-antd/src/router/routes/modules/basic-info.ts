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
      title: $t('basic-info.title'),
    },
    name: 'basic-info',
    path: '/basic-info',
    children: [
      {
        meta: {
          icon: 'mdi:database-outline',
          title: $t('basic-info.database'),
        },
        name: 'basic-info-database',
        path: '/basic-info/database',
        component: () => import('#/views/basic-info/database.vue'),
      },
    ],
  },
];

export default routes;
