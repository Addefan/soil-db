<template>
  <div>
    <Multiselect v-model="value" :options="variants" :multiple="true" :close-on-select="false"
                 :clear-on-select="false" :preserve-search="true" placeholder="Выберите"
                 select-label="" deselect-label="">
    </Multiselect>
  </div>
</template>

<script>
import Multiselect from "vue-multiselect";
import { mapMutations, mapState } from "vuex";

export default {
  name: "SearchSelect",
  components: {
    Multiselect
  },
  computed: {
    value: {
      set(value) {
        this.setParameter({ param: this.attrName, values: value });
      },
      get() {
        return this.parameters[this.attrName] ?? [];
      }
    },
    ...mapState(["parameters"])
  },
  props: {
    variants: Array,
    attrName: { type: String, required: true }
  },
  methods: {
    ...mapMutations({setParameter: "SET_PARAMETER"})
  }
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>
