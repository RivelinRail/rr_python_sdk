std::size_t payload_length_to_device(MsgType_ToDevice msg) {
    switch (msg) {
        case MsgType_ToDevice::Ping: return MsgInfoToDevice<MsgType_ToDevice::Ping>::Length;
        case MsgType_ToDevice::RecordCalibrationPointTangential: return MsgInfoToDevice<MsgType_ToDevice::RecordCalibrationPointTangential>::Length;
        case MsgType_ToDevice::RecordCalibrationPointNormal: return MsgInfoToDevice<MsgType_ToDevice::RecordCalibrationPointNormal>::Length;
        case MsgType_ToDevice::RequestCalibrationPointsTangential: return MsgInfoToDevice<MsgType_ToDevice::RequestCalibrationPointsTangential>::Length;
        case MsgType_ToDevice::RequestCalibrationPointsNormal: return MsgInfoToDevice<MsgType_ToDevice::RequestCalibrationPointsNormal>::Length;
        case MsgType_ToDevice::ACK: return MsgInfoToDevice<MsgType_ToDevice::ACK>::Length;
        case MsgType_ToDevice::ClearLoadCellCalibrationPointsTangential: return MsgInfoToDevice<MsgType_ToDevice::ClearLoadCellCalibrationPointsTangential>::Length;
        case MsgType_ToDevice::ClearLoadCellCalibrationPointsNormal: return MsgInfoToDevice<MsgType_ToDevice::ClearLoadCellCalibrationPointsNormal>::Length;
        case MsgType_ToDevice::EnterLoadCellCalibrationModeTangential: return MsgInfoToDevice<MsgType_ToDevice::EnterLoadCellCalibrationModeTangential>::Length;
        case MsgType_ToDevice::EnterLoadCellCalibrationModeNormal: return MsgInfoToDevice<MsgType_ToDevice::EnterLoadCellCalibrationModeNormal>::Length;
        case MsgType_ToDevice::ExitLoadCellCalibrationModeTangential: return MsgInfoToDevice<MsgType_ToDevice::ExitLoadCellCalibrationModeTangential>::Length;
        case MsgType_ToDevice::ExitLoadCellCalibrationModeNormal: return MsgInfoToDevice<MsgType_ToDevice::ExitLoadCellCalibrationModeNormal>::Length;
        case MsgType_ToDevice::WriteCalibrationCoefficientsTangential: return MsgInfoToDevice<MsgType_ToDevice::WriteCalibrationCoefficientsTangential>::Length;
        case MsgType_ToDevice::WriteCalibrationCoefficientsNormal: return MsgInfoToDevice<MsgType_ToDevice::WriteCalibrationCoefficientsNormal>::Length;
        case MsgType_ToDevice::RecordOrientationCalibrationPoint: return MsgInfoToDevice<MsgType_ToDevice::RecordOrientationCalibrationPoint>::Length;
        case MsgType_ToDevice::ClearOrientationCalibrationPoint: return MsgInfoToDevice<MsgType_ToDevice::ClearOrientationCalibrationPoint>::Length;
        case MsgType_ToDevice::RequestOrientationCalibrationData: return MsgInfoToDevice<MsgType_ToDevice::RequestOrientationCalibrationData>::Length;
        case MsgType_ToDevice::SetAngleOffsetCalibration: return MsgInfoToDevice<MsgType_ToDevice::SetAngleOffsetCalibration>::Length;
        case MsgType_ToDevice::Handshake: return MsgInfoToDevice<MsgType_ToDevice::Handshake>::Length;
        case MsgType_ToDevice::NAK: return MsgInfoToDevice<MsgType_ToDevice::NAK>::Length;
        case MsgType_ToDevice::WriteConfigToFlash: return MsgInfoToDevice<MsgType_ToDevice::WriteConfigToFlash>::Length;
        case MsgType_ToDevice::RequestAngle: return MsgInfoToDevice<MsgType_ToDevice::RequestAngle>::Length;
        case MsgType_ToDevice::RequestConfig: return MsgInfoToDevice<MsgType_ToDevice::RequestConfig>::Length;
        case MsgType_ToDevice::WriteConfig: return MsgInfoToDevice<MsgType_ToDevice::WriteConfig>::Length;
        case MsgType_ToDevice::StartDataStreaming: return MsgInfoToDevice<MsgType_ToDevice::StartDataStreaming>::Length;
        case MsgType_ToDevice::StopDataStreaming: return MsgInfoToDevice<MsgType_ToDevice::StopDataStreaming>::Length;
        case MsgType_ToDevice::RequestFaultData: return MsgInfoToDevice<MsgType_ToDevice::RequestFaultData>::Length;
        case MsgType_ToDevice::ClearFault: return MsgInfoToDevice<MsgType_ToDevice::ClearFault>::Length;
        case MsgType_ToDevice::UpdateSetForce: return MsgInfoToDevice<MsgType_ToDevice::UpdateSetForce>::Length;
        case MsgType_ToDevice::Home: return MsgInfoToDevice<MsgType_ToDevice::Home>::Length;
        case MsgType_ToDevice::RequestDeviceInfo: return MsgInfoToDevice<MsgType_ToDevice::RequestDeviceInfo>::Length;
        case MsgType_ToDevice::JogMotor: return MsgInfoToDevice<MsgType_ToDevice::JogMotor>::Length;
        case MsgType_ToDevice::ToggleLED: return MsgInfoToDevice<MsgType_ToDevice::ToggleLED>::Length;
        case MsgType_ToDevice::AbortMove: return MsgInfoToDevice<MsgType_ToDevice::AbortMove>::Length;
        case MsgType_ToDevice::RequestOrientation: return MsgInfoToDevice<MsgType_ToDevice::RequestOrientation>::Length;
        case MsgType_ToDevice::RequestCurrentForceData: return MsgInfoToDevice<MsgType_ToDevice::RequestCurrentForceData>::Length;
        case MsgType_ToDevice::RequestAccelerationData: return MsgInfoToDevice<MsgType_ToDevice::RequestAccelerationData>::Length;
        case MsgType_ToDevice::Restart: return MsgInfoToDevice<MsgType_ToDevice::Restart>::Length;
        case MsgType_ToDevice::ResetToDefaults: return MsgInfoToDevice<MsgType_ToDevice::ResetToDefaults>::Length;
        case MsgType_ToDevice::StartForceControl: return MsgInfoToDevice<MsgType_ToDevice::StartForceControl>::Length;
        case MsgType_ToDevice::FirmwareUpdateStart: return MsgInfoToDevice<MsgType_ToDevice::FirmwareUpdateStart>::Length;
        case MsgType_ToDevice::FirmwareUpdateChunk: return MsgInfoToDevice<MsgType_ToDevice::FirmwareUpdateChunk>::Length;
        case MsgType_ToDevice::FirmwareUpdateFinalise: return MsgInfoToDevice<MsgType_ToDevice::FirmwareUpdateFinalise>::Length;
        case MsgType_ToDevice::ResetAllCalibrationData: return MsgInfoToDevice<MsgType_ToDevice::ResetAllCalibrationData>::Length;
        case MsgType_ToDevice::ZeroForces: return MsgInfoToDevice<MsgType_ToDevice::ZeroForces>::Length;
        default: return 0;
    }
}

std::size_t payload_length_to_host(MsgType_ToHost msg) {
    switch (msg) {
        case MsgType_ToHost::CalibrationPointNormal: return MsgInfoToHost<MsgType_ToHost::CalibrationPointNormal>::Length;
        case MsgType_ToHost::CalibrationPointTangential: return MsgInfoToHost<MsgType_ToHost::CalibrationPointTangential>::Length;
        case MsgType_ToHost::ACK: return MsgInfoToHost<MsgType_ToHost::ACK>::Length;
        case MsgType_ToHost::Handshake: return MsgInfoToHost<MsgType_ToHost::Handshake>::Length;
        case MsgType_ToHost::OrientationCalibrationData: return MsgInfoToHost<MsgType_ToHost::OrientationCalibrationData>::Length;
        case MsgType_ToHost::ERR: return MsgInfoToHost<MsgType_ToHost::ERR>::Length;
        case MsgType_ToHost::Reserved1: return MsgInfoToHost<MsgType_ToHost::Reserved1>::Length;
        case MsgType_ToHost::AllCalibrationData: return MsgInfoToHost<MsgType_ToHost::AllCalibrationData>::Length;
        case MsgType_ToHost::ConfigData: return MsgInfoToHost<MsgType_ToHost::ConfigData>::Length;
        case MsgType_ToHost::CurrentData: return MsgInfoToHost<MsgType_ToHost::CurrentData>::Length;
        case MsgType_ToHost::FaultData: return MsgInfoToHost<MsgType_ToHost::FaultData>::Length;
        case MsgType_ToHost::DeviceInfo: return MsgInfoToHost<MsgType_ToHost::DeviceInfo>::Length;
        case MsgType_ToHost::OrientationData: return MsgInfoToHost<MsgType_ToHost::OrientationData>::Length;
        case MsgType_ToHost::AccelerationData: return MsgInfoToHost<MsgType_ToHost::AccelerationData>::Length;
        default: return 0;
    }
}
