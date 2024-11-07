import React, { useState } from "react";
import { Button, Modal, Upload, Form, Input, message } from "antd";
import type { UploadFile } from "antd";
import { Image } from "@nextui-org/react";
import axios from "axios";

const NewUser: React.FC<ComponentProps> = ({ onClose }) => {
  const [previewVisible, setPreviewVisible] = useState(false);
  const [previewImage, setPreviewImage] = useState<string | null>(null);
  const [isloading, setIsloading] = useState(false);
  const [messageApi, contextHolder] = message.useMessage();

  const handlePreview = async (file: UploadFile) => {
    let src = file.url as string;
    if (!src && file.originFileObj) {
      src = await new Promise((resolve) => {
        const reader = new FileReader();
        reader.readAsDataURL(file.originFileObj as Blob);
        reader.onload = () => resolve(reader.result as string);
      });
    }
    setPreviewImage(src);
    setPreviewVisible(true);
  };

  const beforeUpload = (file: File) => {
    const isValidType =
      file.type === "image/png" ||
      file.type === "image/jpeg" ||
      file.type === "image/webp"; // Adjusted for "image/jpeg"
    if (!isValidType) {
      messageApi.open({
        type: "error",
        content: `${file.name} is not a png file`,
      });
      return Upload.LIST_IGNORE;
    }
    return false;
  };

  const normFile = (e: any) => {
    if (Array.isArray(e)) {
      return e;
    }
    return e?.fileList;
  };

  const onFinish = async (values: any) => {
    setIsloading(true);
    const formData = new FormData();
    if (values.user) {
      formData.append("name", values.user.name);
      formData.append("note", values.user.note || "");
    }
    values.upload.forEach((file: UploadFile) => {
      if (file.originFileObj) {
        formData.append("images", file.originFileObj);
      }
    });

    // for (let [key, value] of formData.entries()) {
    //   if (value instanceof File) {
    //     console.log(`${key}: ${value.name} (${value.size} bytes)`);
    //   } else {
    //     console.log(`${key}: ${value}`);
    //   }
    // }

    try {
      const res = await axios.post(
        "http://localhost:8000/api/v1/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      if (res.status === 201) {
        await messageApi.open({
          type: "success",
          content: "Image uploaded successfully!",
          duration: 1,
        });
        setIsloading(false);
        onClose();
      }
    } catch (error) {
      setIsloading(false);
      console.log(error);
    }
  };

  return (
    <>
      {contextHolder}
      <Form
        {...layout}
        name="nest-messages"
        onFinish={onFinish}
        style={{ maxWidth: 600 }}
        validateMessages={validateMessages}
      >
        <Form.Item
          name={["user", "name"]}
          label="Name"
          rules={[{ required: true }]}
        >
          <Input />
        </Form.Item>
        <Form.Item name={["user", "note"]} label="Note">
          <Input.TextArea />
        </Form.Item>
        <Form.Item
          name="upload"
          label="Images"
          valuePropName="fileList"
          getValueFromEvent={normFile}
          extra=".jpg .jpeg .png .webp"
          rules={[{ required: true }]}
        >
          <Upload
            name="logo"
            listType="picture"
            multiple={true}
            beforeUpload={beforeUpload}
            onPreview={handlePreview}
          >
            <Button>Click to upload</Button>
          </Upload>
        </Form.Item>
        <Form.Item wrapperCol={{ ...layout.wrapperCol, offset: 4 }}>
          <Button
            type="primary"
            htmlType="submit"
            className="mt-4"
            loading={isloading}
          >
            Start encoding images.
          </Button>
        </Form.Item>
      </Form>
      <Modal
        open={previewVisible}
        title="Image Preview"
        footer={null}
        onCancel={() => setPreviewVisible(false)}
        className="flex justify-center items-center"
      >
        <Image alt="Cropped Preview" isZoomed src={previewImage || ""} />
      </Modal>
    </>
  );
};

export default NewUser;

interface ComponentProps {
  onClose: () => void;
}

const layout = {
  labelCol: { span: 4 },
  wrapperCol: { span: 16 },
};

const validateMessages = {
  required: "${label} is required!",
  types: {
    email: "${label} is not a valid email!",
    number: "${label} is not a valid number!",
  },
  number: {
    range: "${label} must be between ${min} and ${max}",
  },
};
