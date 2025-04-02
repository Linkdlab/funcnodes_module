// IMPORTANT: Do not import anything that itself imports react,
// since in the current state the plugin sytem works only by using the passed React
// this hopefully changes in the future since it limits the plugin system a lots
import { v1_types } from "@linkdlab/funcnodes_react_flow";

const renderpluginfactory = ({ React
  fnrf_zst
  NodeContext
 }: v1_types.RenderPluginFactoryProps) => {
  const MyRendererPlugin: v1_types.RendererPlugin = {
    input_renderers:  {}, // ?: { [key: string]: v1_types.InputRendererType | undefined };
  output_renderers:  {}, // ?: { [key: string]: v1_types.OutputRendererType | undefined };
  handle_preview_renderers:  {}, // ?: { [key: string]: v1_types.HandlePreviewRendererType | undefined };
  data_overlay_renderers:  {}, // ?: { [key: string]: v1_types.DataOverlayRendererType | undefined };
  data_preview_renderers:  {}, // ?: { [key: string]: v1_types.DataPreviewViewRendererType | undefined };
  data_view_renderers:  {}, // ?: { [key: string]: v1_types.DataViewRendererType | undefined };
  node_renderers:  {}, // ?: { [key: string]: v1_types.NodeRendererType | undefined };
  node_context_extenders:  {}, // ?: { [key: string]: v1_types.NodeContextExtenderType | undefined };
  node_hooks:  {}, // ?: { [key: string]: v1_types.NodeHooksType[] | undefined };
  };

  return MyRendererPlugin;
};

const Plugin: v1_types.FuncNodesReactPlugin= {
  renderpluginfactory: renderpluginfactory,
  v: 1,
};

export default Plugin;
