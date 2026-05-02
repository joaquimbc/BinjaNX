meta:
  id: ini1
  endian: le

types:
  ini1_header:
    seq:
      - id: magic
        contents: "INI1"
        
      - id: size
        type: u4
      - id: kip_count
        type: u4
        doc: "Must be smaller than 0x53"
      - id: reserved
        type: u4
        
  kip1_segment:
    seq:
      - id: offset
        type: u4
        
      - id: size
        type: u4
      
      - id: compressed_size
        type: u4
  
  kip1_header:
    seq:
      - id: magic
        contents: "KIP1"
        
      - id: name
        type: strz
        encoding: ascii
        size: 0xC
      
      - id: program_id
        type: u8
        
      - id: version
        type: u4
      
      - id: mthread_priority
        type: u1
        
      - id: mthread_core_num
        type: u1
      
      - id: reserved0
        type: u1
        
      - id: flags
        type: u1
        
      - id: text_segment
        type: kip1_segment
      
      - id: mthread_affinity_mask
        type: u4
      
      - id: ro_segment
        type: kip1_segment
      
      - id: mthread_stack_size
        type: u4
        
      - id: data_segment
        type: kip1_segment
      
      - id: reserved1
        type: u4
    
      - id: bss_segment
        type: kip1_segment
      
      - id: reserved2
        size: 0x24
        
      - id: kernel_capabilities
        size: 0x80
        
    instances:
      total_size:
        value: text_segment.compressed_size + ro_segment.compressed_size + data_segment.compressed_size + bss_segment.compressed_size
        
  
  kip1_program:
    seq:
      - id: header
        size: 0x100
        type: kip1_header
        
      - id: body
        size: header.total_size
seq:
  - id: ini1_file_header
    type: ini1_header
  
  - id: kip1_program
    type: kip1_program
    repeat: expr
    repeat-expr: ini1_file_header.kip_count