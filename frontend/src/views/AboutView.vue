<template>
  <div class="about">
    <h1>This is an about page</h1>
    <p class="text-long">
      This project is mainly meant as a personal budget tracker, thus it won't involve personal data.
      With this idea in mind, more and more features are going to be implemented as deemed appropriate.
    </p>
    <p class="text-long">
      As I was without a job for a long time with my wife working to keep us both afloat, 
      there was a growing need for a tool that could simply analyze/show savings and expenditures in a simple way.
      As graphs are easy to implement these days, labraries like <span class="text-code">pandas</span>, 
      <span class="text-code">matplotlib</span>, <span class="text-code">seaborn</span> etc. are utilized to show current budget status.
    </p>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
