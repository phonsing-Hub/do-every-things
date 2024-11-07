import { useState, useEffect } from "react";
import axios from "axios";
import { Table } from "antd";
import { Avatar, AvatarGroup, Button } from "@nextui-org/react";
import type { TableProps } from "antd";
import { MdEditSquare } from "react-icons/md";
import FormModel from "../form/FormModel";

interface DataType {
  key: number;
  name: string;
  image_name: string;
  note: string;
}
const columns: TableProps<DataType>["columns"] = [

  {
    title: "Name",
    dataIndex: "name",
    render: (name) => <a>{name}</a>,
  },
  {
    title: "Images",
    dataIndex: "image_name",
    render: (image_name) => (
      <AvatarGroup isBordered>
        {image_name.map((image: string, index: number) => (
          <Avatar
            src={`http://127.0.0.1:8000/${image}`}
            key={`${image}-${index}`}
          />
        ))}
      </AvatarGroup>
    ),
  },
  {
    title: "Note",
    dataIndex: "note",
  },
  {
    title: "Action",
    className: "w-32",
    render: () => (
      <Button
        color="primary"
        size="sm"
        radius="sm"
        variant="light"
        startContent={<MdEditSquare size={20} className="text-default-500" />}
      >
        Edit
      </Button>
    ),
  },
];

function New() {
  const [data, setData] = useState([]);
  const getUser = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/v1/images");
      if (res.status === 200) {
        setData(res.data);
      }
    } catch (error) {
      console.log(error);
    }
  };
  useEffect(() => {
    getUser();
  }, []);

  return (
    <section className="py-10 px-4 " id="Home">
      <h2 className="text-3xl">Employess</h2>
      <br />
      <div id="video" className="">
        <div className="mx-auto max-w-full">
          <Table<DataType>
            columns={columns}
            dataSource={data}
            bordered
            title={() => (
              <div className="flex justify-end">
                <FormModel />
              </div>
            )}
            footer={() => (
              <p className="font-bold text-xs text-default-400">ADET @V 0.1.0</p>
            )}
          />
        </div>
      </div>
    </section>
  );
}

export default New;
