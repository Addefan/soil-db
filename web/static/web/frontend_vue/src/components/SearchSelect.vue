<template>
  <div>
    <!--TODO у лейблов bind не нужен, можно просто пустую строку вписать-->
    <!--TODO пишите все интерфейсные сообщения на русском-->
    <Multiselect v-model="value" :options="variants" :multiple="true" :close-on-select="false"
                 :clear-on-select="false" :preserve-search="true" placeholder="Pick some"
                 :select-label="''" :deselect-label="''">
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
        // TODO нельзя использовать commit напрямую

        this.$store.commit("SET_PARAMETER", { param: this.attrName, values: value });
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
    // TODO не говоря о том, что мутации нельзя использовать напрямую, если уж вы маппите что-то, то исползуйте из
    //  this, а не через $store
    ...mapMutations(["SET_PARAMETER"])
  }
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>
