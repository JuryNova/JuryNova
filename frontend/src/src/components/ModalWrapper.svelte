<script>
  import AddCsvModal from "./AddCSVModal.svelte";
  import toast, { Toaster } from "svelte-french-toast";
  import AddModal from "./AddModal.svelte";
</script>

<Toaster />
<AddModal />
<AddCsvModal />

<slot />
