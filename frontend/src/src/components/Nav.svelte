<script>
  import { push } from "svelte-spa-router";
  import store from "../store/store";
  
  let search = "";
  
  const handleSearch = () => {
    window.location.href = `/#/search/${search}`;
    window.location.reload();
  };
  
  const openAddModal = () => {
    $store.isAddModalOpen = true;
  };
  
  const openAddCSVModal = () => {
    $store.isAddCSVModalOpen = true;
  };
</script>

<nav class="container mx-auto px-4 py-3">
  <div class="flex flex-col md:flex-row md:items-center w-full gap-4">
    <!-- Logo -->
    <button
      on:click={() => push("/")}
      class="text-5xl font-bold hover:text-primary transition-colors"
      aria-label="Go to homepage"
    >
      JuryNova.
    </button>

    <!-- Search Form -->
    <div class="md:ml-auto">
      <form
        on:submit|preventDefault={handleSearch}
        class="join w-full max-w-md"
        role="search"
      >
        <input
          type="search"
          class="input w-full input-bordered join-item focus:outline-primary"
          placeholder="Search documents..."
          aria-label="Search documents"
          bind:value={search}
        />
        <button class="btn join-item" type="submit" aria-label="Search">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-6 h-6"
            aria-hidden="true"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
            />
          </svg>
        </button>
      </form>
    </div>

    <!-- Action Buttons -->
    <div class="flex gap-3">
      <button
        on:click={() => push("/config")}
        class="btn btn-circle hover:btn-primary"
        aria-label="Configure Hackathon"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-6 h-6"
          aria-hidden="true"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z"
          />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
          />
        </svg>
      </button>

      <button
        on:click={openAddModal}
        class="btn btn-circle hover:btn-primary"
        aria-label="Add Single Document"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-6 h-6"
          aria-hidden="true"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M12 4.5v15m7.5-7.5h-15"
          />
        </svg>
      </button>

      <button
        on:click={openAddCSVModal}
        class="btn btn-circle hover:btn-primary"
        aria-label="Add CSV File"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-6 h-6"
          aria-hidden="true"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m3.75 9v6m3-3H9m1.5-12H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"
          />
        </svg>
      </button>
    </div>
  </div>
</nav>

<style>
  :global(.tooltip) {
    position: relative;
  }
  
  :global(.tooltip:hover::after) {
    content: attr(aria-label);
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    padding: 0.5rem;
    background: hsl(var(--b3));
    border-radius: 0.5rem;
    font-size: 0.875rem;
    white-space: nowrap;
    z-index: 10;
  }
</style>