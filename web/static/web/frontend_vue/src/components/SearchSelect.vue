<template>
  <div>
    <Multiselect v-model="value" :options="variants" :multiple="true" :close-on-select="false" :clear-on-select="false"
                 :preserve-search="true" placeholder="Pick some" label="name" track-by="name" :preselect-first="false"
                 @close="$emit('add', {'val': value, 'key': field_key})"
                 @remove="$emit('delete', {'val': value, 'key': field_key})">
    </Multiselect>
  </div>
</template>

<script>
import Multiselect from 'vue-multiselect'

export default {
  name: 'SearchSelect',
  components: {
    Multiselect
  },
  data() {
    return {
      value: [],
    }
  },
  props: {
    variants: Array,
    field_key: String,
  },
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>