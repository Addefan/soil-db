<template>
  <div class="flex-wrapper table-color m-0 rounded-4">
    <table class="table table-hover table-bordered vh-100 border-light">
      <thead class="thead-dark rounded-4">
      <tr class="content-align">
        <th scope="col">Уникальный номер</th>
        <th scope="col">Наименование растения</th>
        <th scope="col">Латинское наименование растения</th>
        <th scope="col">Род</th>
        <th scope="col">Организация</th>
      </tr>
      </thead>
      <tbody>
        <tr class="content-align" v-for="plant in this.$store.state.plants" :key="plant">
          <td><a href="" style="color: #000">{{ plant.number }}</a></td>
          <td>{{ plant.name }}</td>
          <td>{{ plant.latin_name }}</td>
          <td>{{ plant.genus }}</td>
          <td>{{ plant.organization }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "plantsTable"
}
</script>

<style scoped>

</style>