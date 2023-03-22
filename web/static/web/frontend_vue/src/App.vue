<script setup>
  import FiltersPanel from "@/components/filtersPanel.vue";
  import PlantsTable from "@/components/plantsTable.vue";
</script>

<template>
  <div class="row">
    <div class="col mb-3 mt-3 pe-1 ms-1">
        <filters-panel></filters-panel>
    </div>
    <div class="col-10 mb-3 mt-3">
        <plants-table></plants-table>
    </div>
  </div>
</template>

<style scoped>

</style>
