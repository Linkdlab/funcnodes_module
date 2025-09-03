// IMPORTANT: Do not import anything that itself imports react,
// since in the current state the plugin sytem works only by using the passed React
// this hopefully changes in the future since it limits the plugin system a lots
import {
  FuncNodesReactPlugin,
  LATEST_VERSION,
  RenderPluginFactoryProps,
  RendererPlugin,
} from "@linkdlab/funcnodes-react-flow-plugin";

const renderpluginfactory = ({}: RenderPluginFactoryProps) => {
  const MyRendererPlugin: RendererPlugin = {
      input_renderers:  {}, // ?: { [key: string]: v1_types.InputRendererType | undefined };
    output_renderers:  {}, // ?: { [key: string]: v1_types.OutputRendererType | undefined };
    handle_preview_renderers:  {}, // ?: { [key: string]: v1_types.HandlePreviewRendererType | undefined };
    data_overlay_renderers:  {}, // ?: { [key: string]: v1_types.DataOverlayRendererType | undefined };
    data_preview_renderers:  {}, // ?: { [key: string]: v1_types.DataPreviewViewRendererType | undefined };
    data_view_renderers:  {}, // ?: { [key: string]: v1_types.DataViewRendererType | undefined };
    node_renderers:  {}, // ?: { [key: string]: v1_types.NodeRendererType | undefined };

  };

  return MyRendererPlugin;
};

const Plugin: FuncNodesReactPlugin = {
  renderpluginfactory: renderpluginfactory,
  v: LATEST_VERSION,
};

export default Plugin;
