import {
  RendererPlugin,
  FuncNodesReactPlugin,
  RenderPluginFactoryProps,
} from "@linkdlab/funcnodes_react_flow";

const renderpluginfactory = ({ React, fnrf_zst }: RenderPluginFactoryProps) => {
  const PlotlyRendererPlugin: RendererPlugin = {
    handle_preview_renderers: {},
    data_overlay_renderers: {},
    data_preview_renderers: {},
    data_view_renderers: {},
    input_renderers: {},
  };

  return PlotlyRendererPlugin;
};

const Plugin: FuncNodesReactPlugin = {
  renderpluginfactory: renderpluginfactory,
};

export default Plugin;
