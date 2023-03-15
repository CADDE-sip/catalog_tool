<template>
  <div class="fit row bg-white q-layout-padding page-container">
    <q-card class="col-grow">
      <q-card-section>
        <div class="text-h6">左のメニューからアクションを選んでください</div>
      </q-card-section>
    </q-card>
  </div>
</template>

<style lang="scss">
.page-container{
  min-height: calc(100vh - 50px);
}

.page-container .q-card{
  height: 20%;
}

.page-container .text-h6{
  color: #1d468f;
}
</style>
