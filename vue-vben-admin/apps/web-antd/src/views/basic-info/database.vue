<script lang="ts" setup>
import type { VxeGridProps } from '#/adapter/vxe-table';

import { Page } from '@vben/common-ui';

import { Button } from 'ant-design-vue';

import { useVbenVxeGrid } from '#/adapter/vxe-table';
import { getDatabaseListApi } from '#/api';

interface RowType {
  id: string;
  host: string;
  username: string;
}

const gridOptions: VxeGridProps<RowType> = {
  columns: [
    { title: 'ID', type: 'seq', width: 50 },
    { field: 'host', title: 'Host' },
    { field: 'username', title: 'Username' },
  ],
  height: 'auto',
  keepSource: true,
  proxyConfig: {
    ajax: {
      query: async ({ page }) => {
        return await getDatabaseListApi({
          page: page.currentPage,
          pageSize: page.pageSize,
        });
      },
    },
  },
  toolbarConfig: {
    refresh: true,
  },
};

const [Grid, gridApi] = useVbenVxeGrid({
  gridOptions,
});
</script>

<template>
  <Page auto-content-height>
    <Grid table-title="Database" table-title-help="Managing Data Sources">
      <template #toolbar-tools>
        <Button type="primary" @click="() => gridApi.reload()">
          Add
        </Button>
      </template>
    </Grid>
  </Page>
</template>