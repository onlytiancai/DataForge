<script lang="ts" setup>
import type { VxeGridProps } from '#/adapter/vxe-table';

import { Page } from '@vben/common-ui';

import { Button } from 'ant-design-vue';

import { useVbenVxeGrid } from '#/adapter/vxe-table';

import { getDatabaseListApi } from '#/api';

interface RowType {
  id: int;
  host: string;
  username: string;
}

const gridOptions: VxeGridProps<RowType> = {
  checkboxConfig: {
    highlight: true,
    labelField: 'name',
  },
  columns: [
    
    { field: 'id', title: 'Product Name' },
    { field: 'host', title: 'Product Name' },
    { field: 'username', title: 'Product Name' },



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
    custom: true,
    // export: true,
    // import: true,
    refresh: true,
    zoom: true,
  },
};

const [Grid, gridApi] = useVbenVxeGrid({
  gridOptions,
});
</script>

<template>
  <Page auto-content-height>
    <Grid table-title="数据列表" table-title-help="提示">
      <template #toolbar-tools>
        <Button class="mr-2" type="primary" @click="() => gridApi.query()">
          Add
        </Button>
      </template>
    </Grid>
  </Page>
</template>