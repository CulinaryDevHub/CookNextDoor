import logo from '../assets/logo.svg';
import { CgProfile } from "react-icons/cg";
import { TfiFacebook } from "react-icons/tfi";
import { FaXTwitter } from "react-icons/fa6";
import { FaInstagram } from "react-icons/fa";
import { FaOpencart } from "react-icons/fa";

const Navbar = () => {
  return (
    <div className='sticky w-full h-36 bg-[#E3F0E7] flex justify-between items-center px-10 text-[#093B31]'>
        <div className='flex justify-between w-96 font-mono font-extralight text-base '>
            <a href="">Menu</a>
            <a href="">Order Online</a>
            <a href="">About</a>
            <a href="">Contact</a>
        </div>
        <div>
            <img src={logo} alt="" className=' size-52' />
        </div>
        <div className='flex justify-between items-center w-[29rem]'>
            <div className='flex justify-between w-20 text-lg'>
                <a href=''>
                    <CgProfile className='size-6'/>
                </a>
                <a href=''>Login</a>
            </div>
            <div className='flex justify-between w-20'>
                <a href=''><TfiFacebook size={'20px'} /></a>
                <a href=''><FaXTwitter size={'20px'}/></a>
                <a href=''><FaInstagram size={'20px'}/></a>
            </div>
            <div>
                <a href=''><FaOpencart size={'22px'}/></a>
            </div>
            <div>
                <button className='w-40 h-11 text-white text-xl bg-[#093B31] hover:bg-[#DE9F7E] hover:text-black hover:border-2 border-black'>Order Online</button>
            </div>
        </div>
    </div>
  )
}

export default Navbar