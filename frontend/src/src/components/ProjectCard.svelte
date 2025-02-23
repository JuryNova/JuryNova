<script>
  import { push } from "svelte-spa-router";
  export let isReviewed = false;
  import ordinal from "ordinal";
  export let index = null;
  export let title = "Project Title";
  export let description = `Lorem ipsum dolor sit amet consectetur, adipisicing elit. Dolorum accusamus
    magni dignissimos nobis ipsam modi deserunt ab? Voluptates repellendus
    placeat doloremque minus, quae, expedita ducimus pariatur atque obcaecati
    perspiciatis distinctio?`;
  export let id = 0;
</script>

<div class="border rounded-md shadow-md h-full flex flex-col">
  <div class="text-2xl p-4 pb-0">{title}</div>
  <div class="mt-4 p-4 pt-0">
    {description}
  </div>
  <div class="flex items-center mt-auto">
    <div class="flex flex-wrap px-4 gap-2">
      {#if isReviewed}
        <div class="tooltip tooltip-bottom" data-tip="Reviewed">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-6 h-6 text-purple-500"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z"
            />
          </svg>
        </div>
      {:else}
        <div class="tooltip tooltip-bottom" data-tip="Not Reviewed">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-6 h-6"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"
            />
          </svg>
        </div>
      {/if}
      {#if index}
        <div class="tooltip tooltip-bottom" data-tip={`Match`}>
          <div class="badge">{ordinal(index)} closest match</div>
        </div>
      {/if}
    </div>
    <button
      on:click={() => push("/project/" + id)}
      class="btn ml-auto m-3 btn-circle btn-sm"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="w-4 h-4"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M4.5 19.5l15-15m0 0H8.25m11.25 0v11.25"
        />
      </svg>
    </button>
  </div>
</div>
