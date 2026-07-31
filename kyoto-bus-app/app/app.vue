<template>
  <div>
    <NuxtRouteAnnouncer />
    <ClientOnly>
      <div id="magnify-target">
        <BusMap />
      </div>
      <MagnifierLens />
    </ClientOnly>
  </div>
</template>
