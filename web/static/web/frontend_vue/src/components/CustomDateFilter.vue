<template>
  <VueDatePicker v-model="date" range locale="ru" cancelText="Закрыть" selectText="Выбрать"
                 :enable-time-picker="false" @update:model-value="$emit('change', date ?? [])"></VueDatePicker>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
export default {
  data() {
    return {
      date: [],
    }
  },
  components: {VueDatePicker},
  name: "CustomDateFilter"
}
</script>

<style scoped>

</style>