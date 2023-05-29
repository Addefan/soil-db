<template>
  <div class="row">
    <div class="col-2 mb-3 mt-3 pe-1">
        <filters-panel></filters-panel>
    </div>
    <div class="col-10 mb-3 mt-3">
        <plants-table></plants-table>
    </div>
  </div>
</template>

<script>
import FiltersPanel from "@/components/FiltersPanel.vue";
import PlantsTable from "@/components/PlantsTable.vue";

export default {
  name: "PlantsView",
  components: { PlantsTable, FiltersPanel }
};
</script>

<style scoped>

</style>