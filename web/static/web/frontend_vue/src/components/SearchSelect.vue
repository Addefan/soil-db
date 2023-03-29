<template>
  <div>
    <Multiselect v-model="value" :options="variants" :multiple="true" :close-on-select="false" :clear-on-select="false"
                 :preserve-search="true" placeholder="Pick some" label="name" track-by="name" :preselect-first="false"
    @select="$emit('change', value)">
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
  },
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>