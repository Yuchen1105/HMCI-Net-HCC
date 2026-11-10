"""Public factory around the preserved source implementation."""


def build_model(config):
    from source.networks.Heiix_Mamba.HM import UXNET
    return UXNET(in_chans=1, out_chans=config["num_classes"], depths=[2, 2, 2, 2],
                 feat_size=[48, 96, 192, 384], drop_path_rate=config["drop_path_rate"],
                 layer_scale_init_value=1e-6, spatial_dims=3)


def load_weights(model, path, device):
    import torch
    checkpoint = torch.load(path, map_location=device, weights_only=True)
    state = checkpoint.get("model", checkpoint.get("state_dict", checkpoint))
    # The preserved model names remain unchanged, including UXNET and HPA3D.
    state = {k.removeprefix("module."): v for k, v in state.items()}
    model.load_state_dict(state, strict=True)
    return checkpoint
